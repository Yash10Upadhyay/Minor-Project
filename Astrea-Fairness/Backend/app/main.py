from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import pandas as pd
from io import BytesIO, StringIO

from app.fairness import run_fairness_audit
from app.scoring import calculate_fairness_score, interpret_bias
from app.utils import validate_columns
from app.mitigation import recommend_mitigation
from app.pdf_report import generate_pdf_report

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

    return {
        **report,
        "fairness_score": score,
        "bias_level": interpret_bias(score),
        "mitigation": mitigation
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