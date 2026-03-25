# Fairness Audit Concepts - Complete Guide

## Table of Contents

- **[Core Concepts](#core-concepts)** - Understanding fairness terms
- **[Configuration](#configuration)** - System setup
- **[Sensitive Attribute](#sensitive-attribute)** - Protected characteristics
- **[Ground Truth Column](#ground-truth-column)** - Actual outcomes
- **[Prediction Column](#prediction-column)** - Model predictions
- **[Complete Example](#complete-example)** - Working example with all components
- **[Fairness Metrics](#fairness-metrics)** - How bias is measured
- **[Real-world Scenarios](#real-world-scenarios)** - Practical applications

---

## Core Concepts

### What is a Fairness Audit?

A fairness audit examines whether decisions made by a system (hiring, lending, promotion, etc.) are fair across different demographic groups.

**Components**:
- **Dataset**: Historical decisions (CSV file with multiple columns)
- **Sensitive Attribute**: Demographic characteristic (e.g., gender, age, race)
- **Ground Truth**: Actual outcome that happened (e.g., hired=yes/no)
- **Prediction**: What the system decided (e.g., hired=yes/no)
- **Analysis**: Compare outcomes across demographic groups

**Question Being Asked**: "Does the system treat people differently based on their demographic characteristics?"

### Example Scenario

```
Hiring Dataset:
===============
Name         | Gender  | Hired | Predicted_Hired
-------------|---------|-------|----------------
Alice        | Female  | Yes   | Yes             ✓ Correct
Bob          | Male    | Yes   | Yes             ✓ Correct
Carol        | Female  | No    | Yes             ✗ Incorrect (False Positive)
Diana        | Female  | Yes   | No              ✗ Incorrect (False Negative)
Ernest       | Male    | Yes   | Yes             ✓ Correct
Frank        | Male    | No    | No              ✓ Correct

Fairness Question: Does the prediction system treat men and women equally?
```

---

## Configuration

### What is Configuration?

**Configuration** refers to the settings and parameters you provide to the fairness audit system to define what's being analyzed and how.

### Configuration Components

#### 1. **DataFrame (Input Data)**
The dataset you're analyzing - typically a CSV file with candidate/applicant records.

**Requirements**:
- Must be a valid CSV file
- Multiple rows (minimum 10+ recommended)
- Multiple columns with different types of information
- Text, numeric, and categorical data

**Example Structure**:
```
CSV File: hiring_candidates.csv
==========================================
candidate_id | name        | gender | age | experience | education | hired
-------------|-------------|--------|-----|------------|-----------|-------
001          | Alice       | Female | 32  | 5 years    | Masters   | Yes
002          | Bob         | Male   | 28  | 3 years    | Bachelor  | Yes
003          | Carol       | Female | 45  | 10 years   | PhD       | No
004          | Diana       | Female | 26  | 1 year     | Bachelor  | No
005          | Ernest      | Male   | 35  | 8 years    | Masters   | Yes
006          | Frank       | Male   | 29  | 4 years    | Bachelor  | No
```

#### 2. **Available Columns**
All column names in your dataset that can be analyzed.

**In Astrea Platform**:
```python
available_columns = ["candidate_id", "name", "gender", "age", 
                    "experience", "education", "hired"]
```

#### 3. **Display Settings**
Configuration of how results are shown.

**Parameters**:
- Chart type (bar, pie, table)
- Number of visualizations
- Detail level (summary vs. detailed)
- Export format (PDF, CSV, JSON)

**Example Configuration**:
```python
config = {
    "display_type": "interactive_tabs",
    "show_metrics": True,
    "show_distributions": True,
    "include_visualizations": True,
    "color_scheme": "professional"
}
```

---

## Sensitive Attribute

### What is a Sensitive Attribute?

A **Sensitive Attribute** is a demographic characteristic that is legally protected or morally important to ensure fair treatment.

### Why It Matters

Discrimination laws protect certain characteristics:
- ❌ Hiring decisions shouldn't be based on gender, race, age
- ❌ Loan decisions shouldn't be based on race, color, national origin
- ❌ Housing shouldn't be based on gender, religion, disability
- ✅ BUT CAN be based on: job qualifications, credit score, income

### Common Sensitive Attributes

#### 1. **Gender**

**Values**: Male, Female, Non-binary, Other
**Legal Protection**: Yes (Title VII in US)
**Why Protected**: Historical discrimination in hiring, pay, promotions

**Example**:
```
Column: gender
Values: ["Male", "Female"]

Analysis Question: 
"Do hiring rates differ between males and females?"

Acceptable: 50% male + 50% female hired
Problematic: 80% male + 20% female hired
```

**Real-world Impact**:
- Women paid 20% less than men for same role
- Women less likely to be hired for technical roles
- Women underrepresented in leadership

#### 2. **Race/Ethnicity**

**Values**: Caucasian, African American, Hispanic, Asian, Native American, Other
**Legal Protection**: Yes (Civil Rights Act 1964)
**Why Protected**: Systemic racism and discrimination

**Example**:
```
Column: race
Values: ["Caucasian", "African American", "Hispanic", "Asian"]

Analysis Question:
"Do hiring rates differ between racial groups?"

Baseline: 70% approval rate overall
- Caucasian: 75% approval (favorable)
- Asian: 70% approval (equal)
- Hispanic: 60% approval (unfavorable)
- African American: 50% approval (unfavorable)

Legal Issue: 4/5 rule violation
If minority < 80% of majority rate = potential discrimination
50/75 = 66.7% < 80% ← VIOLATION
```

#### 3. **Age**

**Values**: Numeric (years) or ranges (18-25, 25-35, 35-50, 50+)
**Legal Protection**: Yes (Age Discrimination in Employment Act)
**Why Protected**: Older workers face "too old" bias

**Example**:
```
Column: age
Values: ["18-25", "25-35", "35-50", "50+"]

Analysis Question:
"Are younger people preferred in hiring?"

Age Group | Hired | Not Hired | Hire Rate
----------|-------|-----------|----------
18-25     | 150   | 50        | 75%  ← Much higher
25-35     | 140   | 60        | 70%
35-50     | 120   | 80        | 60%
50+       | 90    | 110       | 45%  ← Much lower

Finding: Age bias detected - older workers systematically excluded
```

#### 4. **Disability Status**

**Values**: Yes/No or disability type
**Legal Protection**: Yes (Americans with Disabilities Act)
**Why Protected**: Prejudice against disabled individuals

**Example**:
```
Column: has_disability
Values: ["Yes", "No"]

Analysis:
Has Disability | Hire Rate
----------------|----------
No              | 65%
Yes             | 25%  ← Much lower

Finding: Significant bias - same qualifications, lower hire rate
```

#### 5. **Religion**

**Values**: Different religions or "No preference"
**Legal Protection**: Yes (Title VII)
**Why Protected**: Religious discrimination in hiring

**Example**:
```
Column: religion
Values: ["Christian", "Muslim", "Jewish", "Hindu", "Atheist"]

Analysis:
If Muslim candidates have 30% hire rate but Christian 70%
= Evidence of religious discrimination
```

### How Sensitive Attributes are Used in Analysis

```python
# In Astrea Platform
sensitive_attribute = "gender"  # Column to analyze by

# Analysis Steps:
1. Split dataset by gender
   - Group 1: Female (N=500)
   - Group 2: Male (N=500)

2. Calculate outcome rates per group
   - Female hire rate: 45/500 = 9%
   - Male hire rate: 60/500 = 12%

3. Calculate disparity
   - Disparity ratio: 9% / 12% = 0.75
   - Interpretation: Females hired at 75% the rate of males
   
4. Check if statistically significant
   - Chi-square test: p-value = 0.005 (significant)
   
5. Flag if suspicious
   - 75% < 80% (4/5 rule threshold)
   - ✓ Potential discrimination detected
```

---

## Ground Truth Column

### What is Ground Truth?

**Ground Truth** is the actual, real-world outcome that happened. It's the "true answer" - what really occurred.

### Why It's Called "Ground Truth"

- **Ground** = Based on reality, actual facts
- **Truth** = True outcome, not prediction or estimate
- Together = "What actually happened in the real world"

### Ground Truth Examples

#### Example 1: Hiring Decisions

```
Ground Truth Column: "hired"
Possible Values: ["Yes", "No"] or [1, 0]

Meaning: Whether the person was actually hired
Status: FACT - This happened (or didn't happen)

Row 1: Alice, hired = "Yes"
  → Alice WAS actually hired ✓
  
Row 2: Bob, hired = "No"
  → Bob was NOT actually hired ✗
```

#### Example 2: Loan Approval

```
Ground Truth Column: "loan_approved"
Possible Values: ["Approved", "Rejected"] or [1, 0]

Meaning: Whether loan was actually approved
Status: FACT - Bank made this decision

Row 1: Person A, loan_approved = "Approved"
  → Loan WAS actually approved ✓
  → (May or may not have defaulted)
  
Row 2: Person B, loan_approved = "Rejected"
  → Loan was NOT approved ✗
  → (Never got a chance to prove creditworthiness)
```

#### Example 3: Promotion Decisions

```
Ground Truth Column: "promoted"
Possible Values: ["Yes", "No"]

Meaning: Whether employee was actually promoted
Status: FACT - This happened (or didn't)

Row 1: Employee X, promoted = "Yes"
  → Employee was promoted ✓
  
Row 2: Employee Y, promoted = "No"
  → Employee was NOT promoted ✗
```

### Key Characteristics of Ground Truth

| Characteristic | Details |
|---|---|
| **Actual** | Based on what really happened, not predictions |
| **Observable** | Can be verified (hiring records, loan documents, etc.) |
| **Binary or Multi-class** | Usually yes/no, approved/rejected, hired/not hired |
| **Historical** | Based on past decisions that were made |
| **Immutable** | Can't change - it's what happened |
| **Complete** | Must have a value for each row |

### Ground Truth vs. Prediction

```
HIRING EXAMPLE
==============================================
Candidate | Gender | Ground_Truth_Hired | Prediction_Hired
----------|--------|-------------------|----------------
Alice     | Female | Yes               | Yes         ✓ Correct
Bob       | Male   | Yes               | Yes         ✓ Correct  
Carol     | Female | No                | Yes         ✗ Wrong (false positive)
Diana     | Female | Yes               | No          ✗ Wrong (false negative)
Ernest    | Male   | No                | No          ✓ Correct

Ground Truth = Column 3 (Actual outcomes)
               These are FACTS from hiring records
               
Prediction   = Column 4 (What model said)
               These are GUESSES made by system
               
Purpose of Fairness Audit:
"Does the system predict fairly across genders?"
Compare outcomes for male vs female candidates
```

### How Ground Truth is Used

```python
# In Astrea Platform
ground_truth_column = "hired"

# Step 1: Load ground truth
ground_truth = dataframe["hired"]
# Values: [Yes, Yes, No, Yes, No, ...]

# Step 2: Split by demographic group
female_ground_truth = dataframe[dataframe["gender"] == "Female"]["hired"]
male_ground_truth = dataframe[dataframe["gender"] == "Male"]["hired"]

# Step 3: Calculate outcomes
female_approval_rate = female_ground_truth.value_counts()["Yes"] / len(female_ground_truth)
# Example: 45 out of 500 = 9%

male_approval_rate = male_ground_truth.value_counts()["Yes"] / len(male_ground_truth)
# Example: 60 out of 500 = 12%

# Step 4: Calculate disparity
disparity = female_approval_rate / male_approval_rate
# Example: 9% / 12% = 0.75

# Step 5: Flag if problematic
if disparity < 0.8:  # 4/5 rule
    print("⚠️ Potential discrimination detected")
```

---

## Prediction Column

### What is Prediction?

**Prediction** is what a machine learning model or decision system predicted/guessed would happen.

### Why Predictions Matter in Fairness Audits

You want to know: "Is the system's algorithm fair?"

- Ground Truth = What actually happened (facts)
- Prediction = What the algorithm said would happen (guesses)
- Fairness Audit = Compare these two across demographic groups

### Prediction Examples

#### Example 1: Hiring Algorithm

```
Company uses ML model to screen resumes:

Prediction Column: "predicted_hired"
Possible Values: ["Yes", "No"] or [1, 0]

Meaning: What the algorithm predicted about hiring
Status: ALGORITHM OUTPUT - System's decision

Row 1: Alice (Female), predicted_hired = "Yes"
  → Algorithm thought Alice should be hired
  
Row 2: Carol (Female), predicted_hired = "No"
  → Algorithm thought Carol should NOT be hired
  
Question: Does algorithm rate females differently than males?
```

#### Example 2: Loan Approval Algorithm

```
Bank uses automated system to assess loan applications:

Prediction Column: "predicted_approval"
Values: [0.92, 0.45, 0.78, ...]  (probability 0-1)
       or ["Approved", "Rejected"]

Meaning: What system predicted about loan approval
Status: SYSTEM RECOMMENDATION

Row 1: Person A (Race X), predicted_approval = 0.95
  → System very confident should approve
  
Row 2: Person B (Race Y), predicted_approval = 0.35
  → System not confident, might reject

Question: Does system treat races equally?
```

#### Example 3: Resume Screening

```
Automated resume screener using AI:

Prediction Column: "screening_score"
Values: [0.0 to 1.0] (higher = better candidate)

Meaning: System's rating of candidate quality
Status: ALGORITHM ASSESSMENT

Row 1: Kevin Johnson (Male name), score = 0.88
  → Algorithm rated highly
  
Row 2: Keisha Johnson (Female name), score = 0.62
  → Algorithm rated lower (same resume!)

Question: Does algorithm have gender bias in name assessment?
```

### Ground Truth vs. Prediction Comparison

```
COMPLETE FAIRNESS AUDIT EXAMPLE
========================================================

Candidate | Gender | Ground_Truth | Prediction | Match?
          |        | (Actual)     | (Algorithm)|
----------|--------|--------------|------------|--------
Alice     | Female | Hired        | Hired      | ✓ Yes
Bob       | Male   | Hired        | Hired      | ✓ Yes
Carol     | Female | Not Hired    | Hired      | ✗ No (False Positive)
Diana     | Female | Hired        | Not Hired  | ✗ No (False Negative)
Ernest    | Male   | Not Hired    | Not Hired  | ✓ Yes
Frank     | Male   | Hired        | Hired      | ✓ Yes

FAIRNESS ANALYSIS BY GENDER:
========================================================

MALE (Bob, Ernest, Frank):
- Correct predictions: 3/3 = 100%
- Hire rate in actual data: 2/3 = 67%

FEMALE (Alice, Carol, Diana):
- Correct predictions: 1/3 = 33%
- Hire rate in actual data: 1/3 = 33%
- Algorithm predicted hire: 2/3 = 67%

FINDING: ⚠️ Algorithm MORE LIKELY to hire females (false positives)
         but less accurate for females (only 33% correct)
         
PROBLEM: Algorithm assumes females should be hired
         but when they are hired, it's often wrong
```

### Types of Prediction Errors

```
When comparing Ground Truth vs Prediction:

Two groups: Male and Female
Outcome: Hired (Yes) or Not Hired (No)

CORRECT PREDICTIONS:
- True Positive: Ground=Yes, Prediction=Yes ✓
  (Hired and algorithm said hired)
  
- True Negative: Ground=No, Prediction=No ✓
  (Not hired and algorithm said not hired)

INCORRECT PREDICTIONS:
- False Positive: Ground=No, Prediction=Yes ✗
  (Not hired but algorithm said YES - too optimistic)
  
- False Negative: Ground=Yes, Prediction=No ✗
  (Hired but algorithm said NO - too pessimistic)

FAIRNESS CONCERN:
Are False Positive and False Negative rates different
between male and female candidates?

Example:
Males:   5% false positive rate, 8% false negative rate
Females: 15% false positive rate, 20% false negative rate ← IMBALANCE

Interpretation:
Algorithm overestimates female qualifications (more false positives)
Algorithm underestimates female qualifications (more false negatives)
= Systematic bias against females
```

### How Prediction is Used

```python
# In Astrea Platform
prediction_column = "hired"

# Step 1: Load predictions
predictions = dataframe["hired"]
# Values: [Yes, Yes, No, Yes, No, ...]

# Step 2: Compare with ground truth
ground_truth = dataframe["actual_hired"]

# Step 3: Calculate accuracy per group
female_mask = dataframe["gender"] == "Female"
female_predictions = predictions[female_mask]
female_ground_truth = ground_truth[female_mask]

female_accuracy = (female_predictions == female_ground_truth).mean()
# Example: 65% accurate for females

male_mask = dataframe["gender"] == "Male"
male_predictions = predictions[male_mask]
male_ground_truth = ground_truth[male_mask]

male_accuracy = (male_predictions == male_ground_truth).mean()
# Example: 85% accurate for males

# Step 4: Check fairness
if abs(female_accuracy - male_accuracy) > 0.05:
    print("⚠️ Algorithm more accurate for one gender")
    print(f"   Female accuracy: {female_accuracy:.1%}")
    print(f"   Male accuracy: {male_accuracy:.1%}")
```

---

## Complete Example

### Scenario: Tech Company Hiring Analysis

#### Dataset Structure

```csv
employee_id,name,gender,age,education,experience_years,
hired,predicted_hired,hired_date
1,Alice Johnson,Female,32,Masters,5,Yes,Yes,2023-01-15
2,Bob Smith,Male,28,Bachelor,3,Yes,Yes,2023-02-20
3,Carol Davis,Female,45,PhD,10,No,Yes,2023-03-10
4,Diana Miller,Female,26,Bachelor,1,No,No,2023-04-05
5,Ernest Wilson,Male,35,Masters,8,Yes,Yes,2023-05-12
6,Frank Brown,Male,29,Bachelor,4,No,No,2023-06-18
7,Grace Lee,Female,31,Masters,6,Yes,Yes,2023-07-25
8,Henry Garcia,Male,40,PhD,12,Yes,No,2023-08-30
```

#### Configuration

```python
config = {
    "dataset_file": "hiring_candidates.csv",
    "analysis_type": "fairness_audit",
    "display_settings": {
        "show_charts": True,
        "show_tables": True,
        "show_recommendations": True
    }
}
```

#### Sensitive Attribute Selection

```python
sensitive_attribute = "gender"

# Why chosen?
- Protected by law (Title VII)
- Historical bias in tech hiring (fewer women)
- Company regulatory compliance requirement
```

#### Ground Truth Selection

```python
ground_truth_column = "hired"

# Why this column?
- Actual outcome: "Yes" = person was hired, "No" = not hired
- Based on real hiring records (verified facts)
- Immutable: already happened in past
- Complete: every candidate has a value

# What it shows:
- Women hired: 3 out of 4 = 75%
- Men hired: 3 out of 4 = 75%
- No disparity in actual hiring outcomes
```

#### Prediction Selection

```python
prediction_column = "predicted_hired"

# Why this column?
- What the algorithm predicted
- Compare with ground truth to check fairness
- Shows if algorithm is biased

# What it shows:
- Women predicted hired: 3 out of 4 = 75%
- Men predicted hired: 3 out of 4 = 75%
- Algorithm matches actual pretty well
```

#### Analysis Results

```
DEMOGRAPHIC PARITY ANALYSIS
=====================================

Group: Female
- Count: 4
- Hired (Ground Truth): 3 out of 4 = 75%
- Predicted Hired: 3 out of 4 = 75%
- Accuracy: 100% (all predictions correct)

Group: Male
- Count: 4
- Hired (Ground Truth): 3 out of 4 = 75%
- Predicted Hired: 3 out of 4 = 75%
- Accuracy: 75% (1 incorrect: Henry)

DISPARITY RATIO:
Female Rate / Male Rate = 75% / 75% = 1.0
✓ EQUAL (No disparity detected)

ACCURACY DISPARITY:
Female: 100%, Male: 75%
Difference: 25 percentage points
⚠️ Algorithm more accurate for women

CONCLUSION:
✓ No hiring bias detected
⚠️ But algorithm more accurate for one gender
   (May become issue with larger dataset)
```

#### Recommendations

```
1. ✓ Hiring outcomes are fair across genders (75% both)

2. ⚠️ Monitor algorithm accuracy gap
   - Female accuracy: 100%
   - Male accuracy: 75%
   - Collect more data to confirm if pattern continues

3. Check other sensitive attributes
   - Age bias? (Diana=26 not hired, others 28-45 mixed)
   - Education bias? (PhD=No hired, others mixed)

4. Review the Henry case
   - Hired despite algorithm saying "No"
   - Why? Was algorithm wrong or was exception made?
   - Could indicate bias in human review
```

---

## Fairness Metrics

### What Are Fairness Metrics?

Quantitative measurements that tell you if a system is fair.

### Key Metrics Used in Astrea

#### 1. **Disparity Ratio** (4/5 Rule)

```
Formula: Minority Approval Rate / Majority Approval Rate

If < 0.80 (80%) = Potential discrimination detected

Example - Gender:
Female hire rate: 40%
Male hire rate: 60%
Ratio: 40% / 60% = 0.67 (67%)

Result: 67% < 80% ✗ DISCRIMINATION LIKELY
```

#### 2. **Demographic Parity**

```
Definition: Are approval rates equal across groups?

Formula: |Rate_Group1 - Rate_Group2| should be close to 0

Example:
Female hire rate: 45%
Male hire rate: 48%
Difference: 3 percentage points (small = good)

Female hire rate: 20%
Male hire rate: 60%
Difference: 40 percentage points (large = bad)
```

#### 3. **Accuracy Parity**

```
Definition: Is the algorithm equally accurate for all groups?

Formula: Calculate prediction accuracy per group, compare

Example:
Female accuracy: 95%
Male accuracy: 87%
Gap: 8 percentage points (should be < 5%)

Interpretation: Algorithm less accurate for males
                (More wrong predictions for males)
```

#### 4. **False Positive Rate Parity**

```
Definition: Does system wrongly approve too many from one group?

False Positive = System says "Yes" but actual is "No"

Example - Loan Approval:
For Women: 15% of rejected applicants were approved (FP rate)
For Men: 8% of rejected applicants were approved (FP rate)

Disparity: 15% vs 8% = Nearly 2x higher false positive for women
Problem: System too lenient toward women
```

#### 5. **False Negative Rate Parity**

```
Definition: Does system wrongly reject too many from one group?

False Negative = System says "No" but actual is "Yes"

Example - Hiring:
For Women: 20% of hired candidates were predicted "reject"
For Men: 10% of hired candidates were predicted "reject"

Disparity: 20% vs 10% = 2x higher false negative for women
Problem: System underestimates women's qualifications
```

---

## Real-world Scenarios

### Scenario 1: Hiring Discrimination Case

```
SITUATION:
A tech company is accused of gender discrimination in hiring.
Female employees claim fewer women are promoted to senior roles.

ASTREA ANALYSIS SETUP:
- Dataset: 5 years of promotion decisions (500 total)
- Sensitive Attribute: gender
- Ground Truth Column: promoted (Yes/No)
- Prediction Column: algorithm_recommended_promotion

ANALYSIS RESULTS:
Women promoted: 30 out of 250 = 12%
Men promoted: 60 out of 250 = 24%

Disparity ratio: 12% / 24% = 0.50 (50%)
4/5 Rule: 50% < 80% = DISCRIMINATION DETECTED ✗

LEGAL IMPLICATION:
Prima facie case of gender discrimination established.
Company unable to explain substantially equivalent business necessity.
Settlement likely required.
```

### Scenario 2: Loan Approval Equity Audit

```
SITUATION:
Bank wants to ensure loan approval algorithm treats races equally.
Regulatory requirement under Fair Housing Act.

ASTREA ANALYSIS SETUP:
- Dataset: 10,000 loan applications over 1 year
- Sensitive Attribute: race/ethnicity
- Ground Truth Column: actually_approved
- Prediction Column: system_recommendation

ANALYSIS RESULTS:
White applicants: 70% approved
Black applicants: 52% approved
Hispanic applicants: 48% approved
Asian applicants: 68% approved

Disparity ratios:
Black vs White: 52% / 70% = 74% ✗ (< 80%)
Hispanic vs White: 48% / 70% = 69% ✗ (< 80%)
Asian vs White: 68% / 70% = 97% ✓ (≥ 80%)

CONCLUSION:
Algorithm has disparate impact on Black and Hispanic applicants.
Must be remedied to comply with Fair Lending Laws.

POTENTIAL CAUSES:
- Zip code (proxy for race)
- Credit history (may reflect past discrimination)
- Income (correlated with race due to systemic inequality)
```

### Scenario 3: College Admissions Equity Check

```
SITUATION:
University auditing admissions algorithm for potential bias.

ASTREA ANALYSIS SETUP:
- Dataset: 50,000 applications (5 years)
- Sensitive Attribute: first_generation_status
- Ground Truth Column: admitted
- Prediction Column: algorithm_score_quartile

ANALYSIS RESULTS:

First-Gen Student Admit Rate: 18%
Non-First-Gen Student Admit Rate: 32%

Disparity: 18% / 32% = 56% ✗

FINDING:
First-generation students accepted at half the rate of others
despite equivalent qualifications.

POSSIBLE EXPLANATIONS:
1. Different admission standards applied?
2. Algorithm weighs factors that disadvantage first-gen?
3. Essay/recommendation biases?
4. School selectivity differences?

NEXT STEPS:
- Investigate which factors drive disparities
- Remove or adjust biased factors
- Re-test algorithm
- Monitor going forward
```

---

## Summary Table: All Concepts

| Concept | What Is It | Example | Purpose |
|---------|-----------|---------|---------|
| **Configuration** | Settings for the audit | File: hiring.csv, Display: Charts | Define what to analyze |
| **Sensitive Attribute** | Protected demographic | "gender" column | Check for discrimination |
| **Ground Truth** | Actual outcome (facts) | Column "hired": Yes/No | Baseline for comparison |
| **Prediction** | System's decision | Column "approved_algorithm": Yes/No | Check if algorithm is fair |
| **Disparity Ratio** | Outcome rate comparison | 40%/50% = 0.8 | Detect legal violations |
| **Accuracy Gap** | Prediction accuracy diff | Women 95% vs Men 85% | Check algorithm fairness |
| **False Positives** | Wrong approvals | System says yes, actually no | Measure over-approval bias |
| **False Negatives** | Wrong rejections | System says no, actually yes | Measure under-approval bias |

---

## How They Work Together: Complete Flow

```
1. CONFIGURATION
   ↓ User selects dataset (hiring_data.csv)
   ↓

2. DATA LOADED
   ↓ System reads file into memory
   ↓

3. SENSITIVE ATTRIBUTE SELECTED
   ↓ User chooses "gender" column
   ↓

4. GROUND TRUTH SELECTED
   ↓ User chooses "hired" column (actual outcomes)
   ↓

5. PREDICTION SELECTED
   ↓ User chooses "algorithm_hired" column (predictions)
   ↓

6. ANALYSIS PERFORMED
   ├─ Split data by gender
   ├─ Calculate approval rates (Ground Truth)
   ├─ Calculate accuracy (Ground Truth vs Prediction)
   ├─ Calculate prediction rates (Prediction only)
   └─ Identify disparities
   ↓

7. RESULTS DISPLAYED
   ├─ Demographic Parity: Are rates equal?
   ├─ Disparity Ratios: How large are differences?
   ├─ Accuracy Gaps: Is algorithm equally accurate?
   ├─ False Positive/Negative: What errors occur?
   └─ Recommendations: What to fix?
   ↓

8. DECISION MADE
   ✓ System is fair → Use as-is
   ⚠️ Minor issues → Monitor closely
   ✗ Major issues → Remediate before deployment
```

---

## Glossary

**Approval Rate**: Percentage of applicants approved (ground truth)
**Bias**: Systematic difference in treatment between groups
**Demographic Parity**: Equal approval rates across groups
**Disparate Impact**: Neutral policy with discriminatory effect
**False Positive**: System approves, reality is rejection
**False Negative**: System rejects, reality is approval
**Ground Truth**: Actual outcome (what really happened)
**Prediction**: System's output (what it said would happen)
**Sensitive Attribute**: Protected demographic characteristic
**True Positive**: System approves, reality is approval
**True Negative**: System rejects, reality is rejection

This guide provides complete understanding of these critical fairness concepts!
