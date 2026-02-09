# ⚖️ Astrea Fairness Audit Platform

A comprehensive AI ethics and algorithmic bias detection platform that audits datasets across multiple dimensions (tabular, text, image, multimodal) to identify and mitigate discrimination and ensure fairness.

## 🌟 Key Features

### 📊 Comprehensive Fairness Analysis
- **7+ Fairness Metrics** - Demographic parity, equal opportunity, calibration, inequality measures
- **5 Bias Checks** - Systematic, opportunity, error rate, quality, and inequality bias detection
- **5 Fairness Assessments** - Legal compliance, calibration, individual/group fairness, procedural fairness
- **Severity Levels** - Color-coded (🟢🟡🟠🔴) for quick risk assessment

### 🎯 Legal Compliance
- **80% Rule Check** - EEOC employment discrimination standard
- **Legal Risk Assessment** - Identifies potential legal violations
- **Compliance Report** - Documentation for regulatory purposes

### 🎨 Interactive Dashboards
- **5-Tab Dashboard** - Overview, detailed metrics, bias checks, fairness assessment, PDF export
- **Interactive Charts** - Plotly-powered visualizations with hover details
- **Color-Coded Insights** - Green/Yellow/Orange/Red severity indicators
- **Metric Explanations** - Detailed interpretation for each fairness metric

### 📚 Multiple Data Types
- **Tabular Data** - Traditional structured datasets (CSV)
- **Text Analysis** - Gender, race, sentiment bias detection
- **Image Analysis** - Demographic representation, visual feature bias
- **Multimodal Data** - Image-caption pair alignment and stereotype detection

### 🛠️ Actionable Recommendations
- **Auto-Generated Fixes** - Specific mitigation strategies
- **Severity-Based Guidance** - Urgent actions for critical issues
- **Best Practices** - Re-sampling, threshold adjustment, feature engineering suggestions

### 📈 Detailed Reporting
- **PDF Export** - Professional audit reports for stakeholders
- **Metric Explanations** - In-app learning for each metric
- **Visual Dashboards** - Charts showing metrics and trends
- **Recommendations** - Prioritized action items

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip/conda

### Installation

1. **Clone the repository**
```bash
cd Astrea-Fairness
```

2. **Install Backend Dependencies**
```bash
cd Backend
pip install -r requirements.txt
```

3. **Start Backend Server**
```bash
uvicorn app.main:app --reload
```
Backend runs on: `http://localhost:8000`

4. **Start Frontend (new terminal)**
```bash
cd Frontend
streamlit run app.py
```
Frontend runs on: `http://localhost:8501`

### Testing with Sample Data
1. Open `http://localhost:8501` in browser
2. Select "Tabular" data type
3. Upload `sample_data/tabular_hiring_bias.csv`
4. Set parameters: sensitive="gender", y_true="hired", y_pred="hired"
5. Review results across all 5 tabs

---

## 📊 Metrics Overview

### Group Fairness Metrics
| Metric | Range | Ideal | Purpose |
|--------|-------|-------|---------|
| **Demographic Parity Diff** | 0-1 | <0.10 | Selection rate fairness |
| **Demographic Parity Ratio** | 0-1 | ≥0.80 | 80% Rule compliance (LEGAL) |
| **Equal Opportunity Diff** | 0-1 | <0.15 | Fair chances for qualified |
| **False Positive Rate Diff** | 0-1 | <0.15 | Fair error distribution |
| **Predictive Parity Diff** | 0-1 | <0.15 | Prediction reliability |

### Individual Fairness Metrics
| Metric | Range | Ideal | Purpose |
|--------|-------|-------|---------|
| **Theil Index** | 0-∞ | <0.10 | Entropy-based inequality |
| **Atkinson Index** | 0-1 | <0.10 | Welfare loss from inequality |

---

## 🔍 Bias Check Results

### 5 Bias Checks Included
1. **Systematic Bias** - Detects consistent group preference
2. **Opportunity Bias** - Tests equal chances for qualified candidates
3. **Error Rate Bias** - Ensures fair mistake distribution
4. **Quality Bias** - Verifies prediction reliability
5. **Inequality Bias** - Measures outcome distribution fairness

Each check returns severity: 🟢 None | 🟡 Minor | 🟠 Moderate | 🔴 Severe

---

## ⚖️ Fairness Assessments

### 5 Comprehensive Assessments
- **Legal Compliance (80% Rule)** - ✓ PASS / ✗ FAIL
- **Individual Fairness** - Similar treatment for similar people
- **Group Fairness** - Equitable treatment across demographics
- **Calibration Fairness** - Prediction accuracy uniformity
- **Procedural Fairness** - Process transparency & contestability

---

## 📈 Dashboard Tabs

### Tab 1: 📊 Audit Results
- Quick metrics overview (Fairness Score, Bias Level)
- Group distribution bar chart
- Selection rates by group
- Dataset statistics

### Tab 2: 📋 Detailed Metrics
- Individual metric cards with values
- Expandable "Learn More" explanations
- Color-coded interpretation
- Metrics line chart showing all 7 metrics

### Tab 3: 🔍 Bias Checks
- Results for each of 5 bias checks
- Severity levels and descriptions
- Visual severity indicators

### Tab 4: ⚖️ Fairness Assessment
- Results for each fairness assessment
- Detailed findings and interpretations
- Auto-generated recommendations with severity levels
- Prioritized action items

### Tab 5: 📄 PDF Report
- Generate professional audit report
- Download for stakeholders
- Includes metrics, findings, recommendations

---

## 🎯 Use Cases

### Employment/Hiring
✅ Gender/race bias in hiring decisions  
✅ 80% Rule compliance check  
✅ Equal opportunity verification  
✅ Salary disparity analysis  

### Lending/Credit
✅ Discrimination in loan approvals  
✅ Fair interest rate assignment  
✅ Equalized error rates  
✅ Credit scoring equity  

### Criminal Justice
✅ Policing fairness  
✅ Bail/sentencing equity  
✅ False accusation rates  
✅ Rehabilitation opportunities  

### Healthcare
✅ Treatment recommendation fairness  
✅ Diagnosis equity  
✅ Resource allocation fairness  
✅ Health outcome equity  

---

## 📁 Sample Datasets

Ready-to-use datasets in `sample_data/`:

1. **tabular_hiring_bias.csv** (50 records)
   - Gender, age, experience, salary, hiring decisions
   - Demonstrates hiring bias patterns

2. **text_bias_samples.txt** (50 samples)
   - Gender, race, occupational bias in text
   - Test text bias detection

3. **image_metadata.csv** (30 records)
   - Image descriptions with demographic context
   - Professional role assignments

4. **multimodal_image_captions.csv** (30 pairs)
   - Image-caption pairs with stereotyping
   - Different language complexity by gender
   - Occupational bias in captions

---

## 📚 Documentation

- **METRICS_GUIDE.md** - Complete fairness metric reference with examples
- **FEATURES_SUMMARY.md** - Overview of all platform features
- **QUICK_REFERENCE.md** - Quick lookup for metrics and decisions

---

## 📊 Project Structure

```
Astrea-Fairness/
├── Backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI endpoints
│   │   ├── fairness.py             # Core fairness metrics
│   │   ├── fairness_explanations.py # NEW: Detailed explanations
│   │   ├── scoring.py              # Bias interpretation
│   │   ├── mitigation.py           # Recommendations
│   │   ├── pdf_report.py           # PDF generation
│   │   ├── preprocessing.py        # Data preprocessing
│   │   ├── text_bias.py            # Text analysis
│   │   ├── image_bias.py           # Image analysis
│   │   ├── multimodal_bias.py      # Multimodal analysis
│   │   └── utils.py                # Utilities
│   └── requirements.txt             # Python dependencies
├── Frontend/
│   └── app.py                       # Streamlit dashboard
├── sample_data/
│   ├── tabular_hiring_bias.csv
│   ├── text_bias_samples.txt
│   ├── image_metadata.csv
│   └── multimodal_image_captions.csv
├── METRICS_GUIDE.md                # Comprehensive metric guide
├── FEATURES_SUMMARY.md             # Feature overview
├── QUICK_REFERENCE.md              # Quick lookup
└── README.md                       # This file
```

---

## 🔧 API Endpoints

### Audit Endpoints
- `POST /audit-dataset/` - Full audit with metrics and detailed report
- `POST /audit-dataset/pdf` - Generate PDF report

### Analysis Endpoints
- `POST /analyze-text/` - Text bias analysis
- `POST /analyze-images/` - Image dataset analysis
- `POST /analyze-multimodal/` - Multimodal (image-caption) analysis

### Documentation Endpoints
- `GET /metrics/explanations/` - Get all metric explanations
- `GET /metrics/explanation/{metric_name}` - Get specific metric
- `POST /fairness-report/` - Generate comprehensive fairness report

---

## 🎨 Technology Stack

### Backend
- **FastAPI** - High-performance API framework
- **Pandas & NumPy** - Data processing
- **SciPy** - Statistical tests
- **ReportLab** - PDF generation
- **Pillow** - Image processing

### Frontend
- **Streamlit** - Interactive dashboard
- **Plotly** - Interactive visualizations
- **Pandas** - Data display

---

## 📖 How to Use

### Step 1: Start the Application
```bash
# Terminal 1: Start Backend
cd Backend && uvicorn app.main:app --reload

# Terminal 2: Start Frontend
cd Frontend && streamlit run app.py
```

### Step 2: Open Dashboard
Visit `http://localhost:8501`

### Step 3: Select Data Type
- Tabular (CSV)
- Text (TXT or paste)
- Image (JPG/PNG + labels)
- Multimodal (CSV with image-caption pairs)

### Step 4: Upload & Configure
- Choose file
- Set sensitive attribute
- Set target variable (if applicable)
- Click "Analyze"

### Step 5: Review Results
- **Audit Results**: Overview and charts
- **Detailed Metrics**: Each metric explained
- **Bias Checks**: Severity levels
- **Fairness Assessment**: Recommendations
- **PDF Report**: Download audit

### Step 6: Take Action
Implement recommendations from fairness assessment

---

## ⚠️ Important Notes

### Legal Compliance
- **80% Rule Violation** (dp_ratio < 0.80) may violate EEOC employment laws
- If red flag: Consult legal team immediately
- Check fairness_assessment for legal compliance status

### Metric Interpretation
- Lower is better for most metrics (except dp_ratio)
- Check metric explanations for context
- Use multiple metrics together (not individually)
- Thresholds vary by use case

### Color Guide
- 🟢 **Green** - Good/Fair/Compliant
- 🟡 **Yellow** - Warning/Investigate
- 🟠 **Orange** - Concerning/Action needed
- 🔴 **Red** - Critical/Legal risk

---

## ✅ Quick Health Check

Run this to verify everything works:

```bash
# 1. Backend starts on http://localhost:8000
uvicorn app.main:app --reload

# 2. Frontend starts on http://localhost:8501
streamlit run app.py

# 3. Upload sample_data/tabular_hiring_bias.csv
# 4. Verify all 5 tabs load correctly
# 5. Check charts render properly
```

---

**Made with ⚖️ for algorithmic fairness**

*Astrea - Goddess of Justice*
