# ⚖️ Astrea Fairness - Quick Reference Card

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
