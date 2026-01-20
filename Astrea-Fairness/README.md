# Dataset Fairness Auditor
off
A cloud-ready AI ethics tool that audits datasets for bias and fairness.

## Features
- Dataset upload (CSV)
- Sensitive attribute selection
- Fairness metrics using Fairlearn
- Bias interpretation

## Run Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
