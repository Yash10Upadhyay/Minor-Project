# Astrea Fairness - Complete Metrics Guide

## Overview
Astrea Fairness is a comprehensive bias detection and fairness audit platform that analyzes datasets across multiple dimensions - tabular, text, image, and multimodal data - to identify and mitigate discrimination.

---

## 📊 Fairness Metrics

### Group Fairness Metrics

#### 1. **Demographic Parity Difference (dp_diff)**
- **What it measures:** The difference in positive prediction rates between demographic groups
- **Formula:** max(P(Y=1|Group=A)) - min(P(Y=1|Group=B))
- **Range:** 0 to 1 (0 is perfect)
- **Ideal value:** < 0.1 (less than 10% difference)
- **Why it matters:** If one group is consistently favored over another in decisions
- **Example:** If 80% of men are hired but only 50% of women are hired, dp_diff = 0.30

#### 2. **Demographic Parity Ratio (dp_ratio) - 80% Rule**
- **What it measures:** The ratio of selection rates (typically minority/majority)
- **Formula:** min(P(Y=1|Group)) / max(P(Y=1|Group))
- **Range:** 0 to 1 (ideally 0.8-1.0)
- **Legal threshold:** ≥ 0.80 (required by EEOC in US)
- **Why it matters:** Legal standard used in employment discrimination cases
- **Example:** If women are hired at 50% rate and men at 75%, ratio = 50/75 = 0.67 (VIOLATES 80% rule)

#### 3. **Equal Opportunity Difference (eo_diff)**
- **What it measures:** Difference in True Positive Rates (approval rates for qualified individuals)
- **Formula:** max(TPR|Group=A) - min(TPR|Group=B)
- **Range:** 0 to 1 (0 is perfect)
- **Ideal value:** < 0.15 (less than 15% difference)
- **Why it matters:** Ensures qualified candidates get equal chances regardless of group
- **Example:** If 90% of qualified men are approved but only 70% of qualified women are, eo_diff = 0.20

#### 4. **False Positive Rate Difference (fpr_diff)**
- **What it measures:** Difference in false alarm rates across groups
- **Formula:** max(FPR|Group=A) - min(FPR|Group=B))
- **Range:** 0 to 1 (0 is perfect)
- **Ideal value:** < 0.15
- **Why it matters:** Prevents one group from being unfairly accused/rejected more often
- **Example:** If 5% of unqualified men wrongly get approved but 15% of unqualified women do, fpr_diff = 0.10

#### 5. **Predictive Parity Difference (pp_diff)**
- **What it measures:** Difference in precision (reliability) across groups
- **Formula:** max(Precision|Group=A) - min(Precision|Group=B))
- **Range:** 0 to 1 (0 is perfect)
- **Ideal value:** < 0.15
- **Why it matters:** Ensures model predictions are equally trustworthy for all groups
- **Example:** If model is 95% accurate for men but 75% accurate for women, pp_diff = 0.20

#### 6. **Equalized Odds**
- **What it measures:** Combined TPR and FPR differences (stricter than EO alone)
- **Range:** 0 to 1 (0 is perfect)
- **Why it matters:** Satisfies both equal opportunity AND false positive rate fairness
- **Note:** Max(EO_diff, FPR_diff)

---

### Individual Fairness Metrics

#### 7. **Theil Index**
- **What it measures:** Entropy-based inequality in outcome distribution
- **Formula:** (1/n) × Σ(yi/μ) × ln(yi/μ) where μ is mean outcome
- **Range:** 0 to ln(n) where n = number of groups
- **Interpretation:**
  - 0.00 = Perfect equality
  - 0.05 = Very good (low inequality)
  - 0.10 = Good (acceptable)
  - 0.20 = Fair (moderate)
  - 0.30+ = Concerning (high inequality)
- **Why it matters:** Captures whether positive outcomes concentrate in specific groups
- **Example:** If 90% of benefits go to one group, Theil index is high

#### 8. **Atkinson Index**
- **What it measures:** Proportion of welfare/well-being lost due to inequality
- **Formula:** 1 - (Σ(yi^(1-ε))^(1/(1-ε))) / μ where ε=elasticity
- **Range:** 0 to 1 (0 is perfect equality)
- **Interpretation:**
  - 0.00 = Perfect equality
  - 0.10 = Minimal welfare loss
  - 0.20 = Acceptable welfare loss
  - 0.50 = Half of potential welfare lost
  - 0.80+ = Severe inequality
- **Why it matters:** Shows societal impact of unfair outcomes
- **Example:** High Atkinson index means society loses well-being due to inequality

---

## 🔍 Bias Checks

### 1. **Systematic Bias Check**
Determines if there's consistent preference for/against a group across all decisions

**Severity Levels:**
- 🟢 **None**: dp_diff < 0.05
- 🟡 **Minor**: 0.05 ≤ dp_diff < 0.15
- 🟠 **Moderate**: 0.15 ≤ dp_diff < 0.25
- 🔴 **Severe**: dp_diff ≥ 0.25

### 2. **Opportunity Bias Check**
Tests if qualified individuals have equal chances across groups

**Severity Levels:**
- 🟢 **None**: eo_diff < 0.10
- 🟡 **Minor**: 0.10 ≤ eo_diff < 0.15
- 🟠 **Moderate**: 0.15 ≤ eo_diff < 0.30
- 🔴 **Severe**: eo_diff ≥ 0.30

### 3. **Error Rate Bias Check**
Ensures mistakes (false positives/negatives) are distributed fairly

**Severity Levels:**
- 🟢 **None**: fpr_diff < 0.10
- 🟡 **Minor**: 0.10 ≤ fpr_diff < 0.15
- 🟠 **Moderate**: 0.15 ≤ fpr_diff < 0.30
- 🔴 **Severe**: fpr_diff ≥ 0.30

### 4. **Outcome Quality Bias Check**
Verifies model predictions are equally reliable for all groups

**Severity Levels:**
- 🟢 **None**: pp_diff < 0.10
- 🟡 **Minor**: 0.10 ≤ pp_diff < 0.15
- 🟠 **Moderate**: 0.15 ≤ pp_diff < 0.30
- 🔴 **Severe**: pp_diff ≥ 0.30

### 5. **Outcome Inequality Check**
Measures overall inequality in outcome distribution

**Severity Levels:**
- 🟢 **None**: theil_index < 0.10
- 🟡 **Minor**: 0.10 ≤ theil_index < 0.15
- 🟠 **Moderate**: 0.15 ≤ theil_index < 0.25
- 🔴 **Severe**: theil_index ≥ 0.25

---

## ⚖️ Fairness Assessments

### 1. **Legal Compliance Check (80% Rule)**
**Criteria:** P(Y=1|minority) / P(Y=1|majority) ≥ 0.80

**Status:**
- ✓ **PASS**: Model meets legal requirements
- ✗ **FAIL**: Model may violate employment discrimination laws

**Importance:** Required by EEOC for fair hiring practices

### 2. **Individual Fairness Assessment**
**Criteria:** Similar individuals should receive similar treatment

**Levels:**
- 🟢 **Excellent**: theil_index < 0.05
- 🟢 **Good**: theil_index < 0.10
- 🟡 **Fair**: theil_index < 0.20
- 🔴 **Poor**: theil_index ≥ 0.20

### 3. **Group Fairness Assessment**
**Criteria:** 
- Demographic parity (equal positive rates)
- Equal opportunity (equal TPR for qualified)
- Equalized odds (equal TPR and FPR)

**Measured by:** dp_diff, eo_diff, fpr_diff

### 4. **Calibration Fairness Assessment**
**Criteria:** Predicted probabilities match actual outcomes

**Quality:**
- 🟢 **Excellent**: < 0.05 error
- 🟢 **Good**: < 0.10 error
- 🟡 **Fair**: < 0.20 error
- 🔴 **Poor**: ≥ 0.20 error

---

## 📈 Metrics Visualization

### What Each Graph Shows

1. **Group Distribution Bar Chart**
   - Shows how many samples per demographic group
   - Unbalanced groups may require stratified analysis

2. **Selection Rate Bar Chart**
   - Shows positive prediction rate per group
   - Should be similar across groups (ideally)
   - If bars differ significantly, demographic parity is violated

3. **Metrics Line Chart**
   - All fairness metrics on one view
   - Lower values = better (fair) for most metrics
   - Except dp_ratio which should be ≥ 0.80

---

## 🎯 Recommended Metric Priorities

### For Hiring/Employment (Primary Priority)
1. **Demographic Parity Ratio** (80% Rule) - LEGAL REQUIREMENT
2. **Equal Opportunity Difference** - Qualified candidates get fair chance
3. **Demographic Parity Difference** - No group systematically favored

### For Lending/Credit
1. **Equalized Odds** - Fair error rates and approval rates
2. **Theil Index** - Ensure opportunities spread fairly
3. **Demographic Parity** - No systematic discrimination

### For Criminal Justice
1. **Equal Opportunity** - Fair treatment of defendants
2. **False Positive Rate Difference** - Avoid unfair accusations
3. **Predictive Parity** - Predictions equally reliable

### For General Purpose
1. **Demographic Parity Difference** - Basic fairness check
2. **Equalized Odds** - Comprehensive fairness
3. **Theil Index** - Inequality assessment
4. **Atkinson Index** - Welfare impact

---

## ⚠️ Interpreting Results

### Green Zone (✓ Good)
- All metrics below thresholds
- Bias checks show "None"
- Legal compliance: PASS
- **Action:** Monitor and continue current practices

### Yellow Zone (⚠️ Warning)
- Some metrics slightly elevated
- Some "Minor" bias detected
- Legal compliance uncertain
- **Action:** Investigate bias sources, plan mitigation

### Orange Zone (⚠️ Concerning)
- Multiple metrics elevated
- Moderate bias detected
- May violate legal requirements
- **Action:** Urgent investigation and remediation needed

### Red Zone (🔴 Critical)
- Metrics significantly elevated
- Severe bias detected
- Legal non-compliance likely
- **Action:** Immediate remediation required, potential legal liability

---

## 🛠️ Common Bias Mitigation Strategies

1. **Re-sampling/Re-weighting**
   - Over-sample underrepresented groups
   - Increase weight for positive cases in minority groups

2. **Threshold Adjustment**
   - Set different decision thresholds per group
   - Balance TPR and FPR within each group

3. **Feature Engineering**
   - Remove proxy variables for sensitive attributes
   - Add features that represent protected groups' experiences

4. **Fairness Constraints**
   - Add constraints during model training
   - Optimize for multiple objectives (accuracy + fairness)

5. **Post-processing**
   - Adjust predictions after model generates them
   - Ensure compliance before decisions made

6. **Data Augmentation**
   - Collect more data from underrepresented groups
   - Ensure training data reflects population diversity

---

## 📚 Additional Data Types

### Text Bias Detection
- **Gender Bias**: Language patterns favoring specific genders
- **Racial Bias**: Stereotyping and racial associations
- **Sentiment Bias**: Positive/negative language tied to demographics

### Image Bias Detection
- **Demographic Representation**: Imbalance in groups represented
- **Visual Feature Bias**: Different treatment based on visual characteristics
- **Color Bias**: Systematic color/lighting differences across groups

### Multimodal Bias Detection
- **Alignment Bias**: Image-caption alignment varies by group
- **Stereotype Detection**: Stereotypical associations in captions
- **Attribution Bias**: Different attribute assignments across groups

---

## 🚀 Quick Start Guide

1. **Upload Dataset** → Select data type and file
2. **Configure Parameters** → Set sensitive attribute, target columns
3. **Run Audit** → Generate fairness metrics
4. **Review Metrics** → Check each fairness metric explanation
5. **Check Bias** → Review bias detection results
6. **Assess Fairness** → Review fairness assessments
7. **Take Action** → Implement recommendations
8. **Export Report** → Download PDF for documentation

---

## 📞 Support & Questions

For detailed metric definitions and fairness theory, consult the in-app explanations for each metric.

**Reference:** Based on fairness frameworks from Microsoft Fairlearn, AI Fairness 360, and academic literature on algorithmic bias and fairness.
