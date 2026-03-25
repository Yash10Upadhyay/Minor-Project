from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import Response
import pandas as pd
from io import BytesIO, StringIO
import json
import ast

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

    # If provided sensitive column does not exist, try to fallback to 'gender'
    if sensitive not in df.columns and "gender" in df.columns:
        sensitive = "gender"

    # Ensure y_true and y_pred exist
    validate_columns(df, [y_true, y_pred])

    report = run_fairness_audit(df, sensitive, y_true, y_pred)
    score = calculate_fairness_score(report["metrics"])

    mitigation = recommend_mitigation(report["metrics"])
    
    # Generate detailed fairness report
    detailed_report = generate_detailed_fairness_report(
        report["metrics"],
        report["group_distribution"]
    )

    # Suggest likely application scenarios by inspecting column names
    scenarios = []
    cols = set(df.columns.str.lower())
    fname = (file.filename or "").lower()
    if any(c for c in ["hire", "hired", "hiring"] if c in cols or c in fname):
        scenarios.append("Hiring decisions / recruitment audits")
    if any(c for c in ["loan", "credit", "approved"] if c in cols or c in fname):
        scenarios.append("Loan approval / credit scoring")
    if any(c for c in ["admit", "admission"] if c in cols or c in fname):
        scenarios.append("Admissions / selection processes")
    if not scenarios:
        scenarios.append("General decision-making / selection audits")
        if not scenarios:
            scenarios.append("General tabular decisioning (e.g., HR, lending, admissions)")

    return {
        **report,
        "fairness_score": score,
        "bias_level": interpret_bias(score),
        "mitigation": mitigation,
        "detailed_report": detailed_report,
        "likely_scenarios": scenarios,
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
async def analyze_images(request: Request):
    """Analyze bias in image datasets using ResNet-based models."""
    try:
        from PIL import Image as PILImage
        import io
        
        # Get form data
        form_data = await request.form()
        
        # Extract demographics from query params
        demographics = request.query_params.get("demographics", "")
        
        # Collect uploaded images
        images = []
        image_files = []
        
        # Iterate through form keys to find all images
        for key in form_data:
            if key.startswith('image_'):
                file = form_data[key]
                if file:
                    try:
                        content = await file.read()
                        img_array = ImagePreprocessor.load_image(content)
                        images.append(img_array)
                        image_files.append(file.filename)
                    except Exception as e:
                        return {"error": f"Failed to load image {file.filename}: {str(e)}"}
        
        if not images:
            return {"error": "No images uploaded"}
        
        # Parse demographics
        if isinstance(demographics, list):
            demographic_groups = demographics
        elif isinstance(demographics, str):
            if demographics.startswith('['):
                # Try JSON format first
                try:
                    demographic_groups = json.loads(demographics)
                except:
                    # Try Python list format: "['male', 'female']"
                    try:
                        demographic_groups = ast.literal_eval(demographics)
                        if not isinstance(demographic_groups, list):
                            demographic_groups = []
                    except:
                        demographic_groups = []
            else:
                # Plain text format (one per line)
                demographic_groups = [line.strip() for line in demographics.strip().split('\n') if line.strip()]
        else:
            demographic_groups = []
        
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