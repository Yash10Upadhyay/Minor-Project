from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import pandas as pd
from io import BytesIO, StringIO

from app.fairness import run_fairness_audit
from app.scoring import calculate_fairness_score, interpret_bias
from app.utils import validate_columns
from app.mitigation import recommend_mitigation
from app.pdf_report import generate_pdf_report
from app.preprocessing import DataPreprocessor, TextPreprocessor, ImagePreprocessor
from app.text_bias import TextBiasAnalyzer
from app.image_bias import ImageBiasAnalyzer
from app.multimodal_bias import MultimodalBiasAnalyzer
from app.fairness_explanations import (
    METRICS_EXPLANATIONS, BIAS_CHECKS, FAIRNESS_CHECKS,
    generate_detailed_fairness_report
)

app = FastAPI(title="Astrea Fairness API")


@app.post("/audit-dataset/")
async def audit_dataset(
    file: UploadFile = File(...),
    sensitive: str = "gender",
    y_true: str = "label",
    y_pred: str = "prediction"
):
    # Read file content as bytes
    content = await file.read()
    
    # Decode to string and use StringIO for CSV
    df = pd.read_csv(StringIO(content.decode('utf-8')))

    validate_columns(df, [sensitive, y_true, y_pred])

    report = run_fairness_audit(df, sensitive, y_true, y_pred)
    score = calculate_fairness_score(report["metrics"])

    mitigation = recommend_mitigation(report["metrics"])
    
    # Generate detailed fairness report
    detailed_report = generate_detailed_fairness_report(
        report["metrics"],
        report["group_distribution"]
    )

    return {
        **report,
        "fairness_score": score,
        "bias_level": interpret_bias(score),
        "mitigation": mitigation,
        "detailed_report": detailed_report,
        "metrics_explanations": METRICS_EXPLANATIONS
    }


@app.post("/audit-dataset/pdf")
async def audit_dataset_pdf(
    file: UploadFile = File(...),
    sensitive: str = "gender",
    y_true: str = "label",
    y_pred: str = "prediction"
):
    # Read file content as bytes
    content = await file.read()
    
    # Check if content is empty
    if not content:
        return {"error": "Empty file uploaded"}
    
    # Decode to string and use StringIO for CSV
    try:
        df = pd.read_csv(StringIO(content.decode('utf-8')))
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}

    validate_columns(df, [sensitive, y_true, y_pred])

    report = run_fairness_audit(df, sensitive, y_true, y_pred)
    score = calculate_fairness_score(report["metrics"])

    full_report = {
        **report,
        "fairness_score": score,
        "bias_level": interpret_bias(score),
        "mitigation": recommend_mitigation(report["metrics"])
    }

    # Create temporary file for PDF
    try:
        # Generate PDF as bytes
        pdf_bytes = generate_pdf_report(full_report)
        
        # Return PDF directly
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=astrea_fairness_report.pdf"}
        )
    except Exception as e:
        return {"error": f"Failed to generate PDF: {str(e)}"}


# ============ TEXT BIAS ANALYSIS ============
@app.post("/analyze-text/")
async def analyze_text(request: dict):
    """Analyze bias in text data using BERT-based NLP models."""
    try:
        texts = request.get("texts", [])
        
        if not texts:
            return {"error": "No texts provided"}
        
        # Run text bias analysis
        analyzer = TextBiasAnalyzer()
        result = analyzer.comprehensive_text_bias_analysis(texts)
        
        return result
    except Exception as e:
        return {"error": f"Failed to analyze text: {str(e)}"}


# ============ IMAGE BIAS ANALYSIS ============
@app.post("/analyze-images/")
async def analyze_images(
    demographics: str = "",
    image_0: UploadFile = File(None),
    image_1: UploadFile = File(None),
    image_2: UploadFile = File(None),
    image_3: UploadFile = File(None),
    image_4: UploadFile = File(None),
    image_5: UploadFile = File(None),
    image_6: UploadFile = File(None),
    image_7: UploadFile = File(None),
    image_8: UploadFile = File(None),
    image_9: UploadFile = File(None),
):
    """Analyze bias in image datasets using ResNet-based models."""
    try:
        import json
        from PIL import Image
        
        # Collect uploaded images
        images = []
        image_files = [image_0, image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9]
        
        for img_file in image_files:
            if img_file:
                try:
                    content = await img_file.read()
                    # Load image from bytes
                    from PIL import Image as PILImage
                    import io
                    pil_image = PILImage.open(io.BytesIO(content))
                    # Convert to numpy array
                    img_array = ImagePreprocessor.normalize_image(
                        ImagePreprocessor.load_image(content)
                    )
                    images.append(img_array)
                except Exception as e:
                    return {"error": f"Failed to load image {img_file.filename}: {str(e)}"}
        
        if not images:
            return {"error": "No images uploaded"}
        
        # Parse demographics
        try:
            demographic_groups = json.loads(demographics) if isinstance(demographics, str) else demographics
        except:
            demographic_groups = demographics if isinstance(demographics, list) else []
        
        if len(images) != len(demographic_groups):
            return {"error": f"Image count ({len(images)}) must match demographic count ({len(demographic_groups)})"}
        
        # Run image bias analysis
        analyzer = ImageBiasAnalyzer()
        result = analyzer.comprehensive_image_bias_analysis(images, demographic_groups)
        
        return result
    except Exception as e:
        return {"error": f"Failed to analyze images: {str(e)}"}


# ============ MULTIMODAL BIAS ANALYSIS ============
@app.post("/analyze-multimodal/")
async def analyze_multimodal(request: dict):
    """Analyze bias in multimodal data (image-caption pairs) using CLIP/VILT models."""
    try:
        image_captions = request.get("image_captions", [])
        demographic_groups = request.get("demographic_groups", [])
        
        if not image_captions or not demographic_groups:
            return {"error": "image_captions and demographic_groups are required"}
        
        if len(image_captions) != len(demographic_groups):
            return {"error": f"Pair count ({len(image_captions)}) must match demographic count ({len(demographic_groups)})"}
        
        # Run multimodal bias analysis
        analyzer = MultimodalBiasAnalyzer()
        result = analyzer.comprehensive_multimodal_bias_analysis(image_captions, demographic_groups)
        
        return result
    except Exception as e:
        return {"error": f"Failed to analyze multimodal data: {str(e)}"}


# ============ EXPLANATIONS & DOCUMENTATION ============
@app.get("/metrics/explanations/")
async def get_metrics_explanations():
    """Get detailed explanations for all fairness metrics."""
    return {
        "metrics_explanations": METRICS_EXPLANATIONS,
        "bias_checks": BIAS_CHECKS,
        "fairness_checks": FAIRNESS_CHECKS
    }


@app.get("/metrics/explanation/{metric_name}")
async def get_metric_explanation(metric_name: str):
    """Get explanation for a specific metric."""
    if metric_name in METRICS_EXPLANATIONS:
        return {metric_name: METRICS_EXPLANATIONS[metric_name]}
    return {"error": f"Metric '{metric_name}' not found"}


@app.post("/fairness-report/")
async def generate_fairness_report(metrics: dict):
    """Generate comprehensive fairness report from metrics."""
    try:
        group_distribution = metrics.get("group_distribution", {})
        metric_values = metrics.get("metrics", {})
        
        report = generate_detailed_fairness_report(metric_values, group_distribution)
        
        return {
            "report": report,
            "metrics_explanations": METRICS_EXPLANATIONS
        }
    except Exception as e:
        return {"error": f"Failed to generate report: {str(e)}"}