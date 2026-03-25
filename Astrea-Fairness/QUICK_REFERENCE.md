# ⚖️ Astrea Fairness Platform - Quick Reference Card

## 🎓 Core Concepts (30 Second Explanation)

### 1. **Configuration**
```
What: Your setup and analysis settings
Why: Tells the system what to analyze and how
Example: "Open my hiring_data.csv file and look for fairness issues"
```

### 2. **Sensitive Attribute**
```
What: Protected demographic characteristic (gender, race, age, etc.)
Why: You're checking if system discriminates against protected groups
Example: gender = ["Male", "Female"] - analyze hiring bias by gender
```

### 3. **Ground Truth Column**
```
What: ACTUAL outcome that happened (facts from history)
Why: Real baseline to measure fairness against
Example: hired = ["Yes", "No"] - who was actually hired (verified fact)
```

### 4. **Prediction Column**
```
What: What algorithm/system PREDICTED would happen
Why: Compare with ground truth to check if algorithm is fair
Example: algorithm_hired = ["Yes", "No"] - system's recommendation
```

### 5. **Fairness Analysis**
```
What: Comparing all 4 above to detect discrimination
Process: Does algorithm treat all [Sensitive Attribute] groups equally?
Result: Bias Score + Recommendations + Visualizations
```

---

## 📊 Essential Metrics (At a Glance)

| Metric | Abbrev | Range | Ideal | What it Measures | Red Flag |
|--------|--------|-------|-------|------------------|----------|
| Demographic Parity Diff | dp_diff | 0-1 | <0.10 | Selection rate difference | >0.20 |
| Demographic Parity Ratio | dp_ratio | 0-1 | ≥0.80 | 80% Rule compliance | <0.80 |
| Equal Opportunity Diff | eo_diff | 0-1 | <0.15 | Fair chances for qualified | >0.30 |
| False Positive Rate Diff | fpr_diff | 0-1 | <0.15 | Fair error distribution | >0.30 |
| Predictive Parity Diff | pp_diff | 0-1 | <0.15 | Prediction reliability | >0.30 |
| Theil Index | theil | 0-∞ | <0.10 | Inequality in outcomes | >0.25 |
| Atkinson Index | atkinson | 0-1 | <0.10 | Welfare loss | >0.20 |

---

## 🔄 How It All Works Together: Complete Flow

```
STEP 1: CONFIGURATION
  ↓ Load your dataset (CSV file)
  
STEP 2: SELECT SENSITIVE ATTRIBUTE
  ↓ Example: Column "gender" with values [Male, Female]
  
STEP 3: SELECT GROUND TRUTH COLUMN
  ↓ Example: Column "hired" = actual hiring decisions
  
STEP 4: SELECT PREDICTION COLUMN
  ↓ Example: Column "algorithm_hired" = algorithm's recommendation
  
STEP 5: SYSTEM ANALYZES
  ├─ Splits data by gender (sensitive attribute)
  ├─ Compares Ground Truth vs Prediction
  ├─ Calculates fairness metrics
  └─ Flags disparities
  
STEP 6: RESULTS DISPLAYED
  ├─ Disparity ratio (< 80% = discrimination)
  ├─ Accuracy differences
  ├─ False positive/negative rates
  └─ Visualizations
  
STEP 7: DECISION MADE
  ✓ Fair? Use system
  ⚠️ Minor issues? Monitor & improve
  ✗ Major bias? Fix before deploying
```

---

## 📋 Real-World Example: Hiring Analysis

```
YOUR SETUP:
  Configuration: hiring_candidates.csv (500 rows)
  Sensitive Attribute: gender = [Male=250, Female=250]
  Ground Truth: hired = [Yes, No] from past hiring records
  Prediction: algorithm_hired = algorithm's recommendations

ANALYSIS RESULTS:
  
  All Candidates:
    Ground Truth: 180 hired out of 500 = 36% hire rate
    
  By Gender:
    Males:   108/250 hired = 43.2% hire rate
    Females: 72/250 hired = 28.8% hire rate
    
  Algorithm Predictions:
    Males predicted hired:   140/250 = 56%
    Females predicted hired: 100/250 = 40%

FAIRNESS METRICS:
  
  Disparity Ratio (Ground Truth):
    28.8% / 43.2% = 0.667 = 67% ← VIOLATION (< 80%) 🔴
    
  Accuracy:
    Males: algorithm correct 77% of the time
    Females: algorithm correct 60% of the time
    Gap: 17 percentage points ⚠️
    
  False Negative Rate (missed qualified candidates):
    Males: 8% of qualified males predicted reject
    Females: 25% of qualified females predicted reject
    Algorithm underestimates women 3x more ✗

LEGAL ASSESSMENT:
  ✗ DISCRIMINATION DETECTED (67% < 80%)
  ✗ Algorithm biased against females
  ✗ Violates Title VII & EEOC guidelines
  
RECOMMENDATION:
  → Immediate remediation required
  → Remove or adjust biased factors
  → Retrain algorithm on balanced data
  → Validate before redeployment
```

---

## 🎯 Quick Decision Guide

### If you see:
- 🟢 **All metrics green** → Model is fair, continue monitoring
- 🟡 **Some yellow** → Investigate bias sources, plan changes
- 🟠 **Orange zones** → Fix required, fairness improvement needed
- 🔴 **Red zones** → Critical issue, immediate remediation required

---

## ⚠️ Severity Color System

| Color | Meaning | What to Do |
|-------|---------|-----------|
| 🟢 Green | Good | Monitor and maintain |
| 🟡 Yellow | Warning | Investigate and plan fix |
| 🟠 Orange | Concerning | Implement remediation |
| 🔴 Red | Critical | Urgent - legal risk |

---

## 📋 5 Bias Checks Explained

| Check | Measures | Green | Red |
|-------|----------|-------|-----|
| Systematic | Consistent group bias | dp_diff <0.05 | dp_diff >0.25 |
| Opportunity | Qualified equal chances | eo_diff <0.10 | eo_diff >0.30 |
| Error Bias | Fair mistake rates | fpr_diff <0.10 | fpr_diff >0.30 |
| Quality | Reliable predictions | pp_diff <0.10 | pp_diff >0.30 |
| Inequality | Fair outcome spread | theil <0.10 | theil >0.25 |

---

## ⚙️ Quick Fixes for Common Issues

### Problem: High dp_diff (Selection rate bias)
**Solution:** 
- Re-weight training data to balance groups
- Adjust decision thresholds per group
- Remove proxy variables

### Problem: Low dp_ratio (80% Rule violation)
**Solution:**
- Urgent: This violates employment law
- Decrease majority group selection OR increase minority group
- Get legal review immediately

### Problem: High eo_diff (Unequal opportunity)
**Solution:**
- Train fairness-aware model
- Use group-specific thresholds
- Review for systemic data bias

### Problem: High fpr_diff (Unfair error rates)
**Solution:**
- Tune classification thresholds per group
- Apply fairness constraints during training
- Use post-processing calibration

### Problem: High theil_index (Inequality)
**Solution:**
- Use stratified fairness constraints
- Ensure diverse training data
- Balance multiple objectives

---

## 🎓 When to Use Each Metric

| Use Case | Primary | Secondary |
|----------|---------|-----------|
| **Hiring/Employment** | dp_ratio, eo_diff | fpr_diff, theil |
| **Lending/Credit** | eo_diff, fpr_diff | pp_diff, atkinson |
| **Criminal Justice** | fpr_diff, eo_diff | pp_diff, theil |
| **Healthcare** | eo_diff, pp_diff | dp_diff, atkinson |
| **Education** | eo_diff, theil | fpr_diff, dp_diff |

---

## 🔍 How to Read Results

### Dashboard Tabs
1. **Audit Results** - See quick overview & charts
2. **Detailed Metrics** - Read explanation for each metric
3. **Bias Checks** - Find specific bias types & severity
4. **Fairness Assessment** - See recommendations
5. **PDF Report** - Download for documentation

### Key Sections in Each Tab
- **Metrics Cards** - Show value + interpretation
- **Charts** - Visual comparison across groups
- **Explanations** - Click "Learn More" for details
- **Recommendations** - Specific action items

---

## 📈 Understanding the Charts

### Group Distribution
Shows sample count per group
- Unbalanced = need stratified analysis
- Balanced = reliable metrics

### Selection Rate by Group
Shows approval/positive rate per group
- Similar heights = good (fair)
- Different heights = bias detected

### Metrics Line Chart
All 7 metrics plotted together
- Lower is better (except dp_ratio)
- Spikes = problem areas
- Flat line = balanced fairness

---

## ✅ Fairness Assessment Results

| Assessment | Good Result | Warning | Critical |
|------------|-------------|---------|----------|
| Legal Compliance | PASS | N/A | FAIL |
| Individual Fairness | Excellent | Fair | Poor |
| Group Fairness | All low diffs | Some high | Major disparities |
| Calibration | < 0.05 error | < 0.10 | > 0.20 |

---

## 🚀 5-Step Quick Start

1. **📤 Upload** CSV/Text/Images
2. **⚙️ Configure** Sensitive attribute & target
3. **▶️ Run** Analysis
4. **📊 Review** Metrics & checks
5. **✏️ Fix** Using recommendations

---

## 📞 Common Questions

**Q: What's the 80% Rule?**  
A: Legal requirement - minority group selection rate ≥ 80% of majority rate

**Q: Which metric matters most?**  
A: Depends on use case (see table above)

**Q: What if dp_ratio < 0.80?**  
A: Likely violates employment law - urgent remediation needed

**Q: Can I use multiple fairness definitions?**  
A: Yes - Astrea checks multiple dimensions for comprehensive fairness

**Q: What does yellow/orange/red mean?**  
A: Yellow=investigate, Orange=fix needed, Red=critical/legal risk

---

## 📚 Documentation Files

- **METRICS_GUIDE.md** - Comprehensive metric explanations
- **FEATURES_SUMMARY.md** - Overview of all features
- **README.md** - General project info
- **This file** - Quick reference

---

## 🎯 Sample Datasets Ready to Use

1. **Hiring bias** - Tabular data with gender bias
2. **Text bias** - Multiple bias types in sentences
3. **Image metadata** - Role assignment by demographics
4. **Multimodal** - Stereotyping in image captions

Located in: `sample_data/` folder

---

**💡 TIP:** Start with sample data to understand how metrics work, then use with your own data!

**⚠️ IMPORTANT:** If dp_ratio < 0.80, consult legal team immediately - potential EEOC violation.

**🎉 Remember:** Fairness is multi-dimensional. Check multiple metrics together!
