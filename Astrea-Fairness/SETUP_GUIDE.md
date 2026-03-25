# 🚀 Astrea Fairness Platform - Complete Setup & Usage Guide

## **Overview**
Astrea Fairness is a comprehensive fairness audit platform that detects bias in:
- ✅ **Tabular Data** (CSV files - hiring, loans, decisions)
- ✅ **Text Data** (Resumes, descriptions, reviews)
- ✅ **Image Data** (Photo datasets)
- ✅ **Multimodal Data** (Image + Caption pairs)

---

## **📋 Prerequisites**

Make sure you have installed:
- Python 3.8+
- pip (Python package manager)

---

## **⚙️ Installation & Setup**

### **Step 1: Install Backend Dependencies**

```bash
cd "d:\Minor Project\Astrea-Fairness\Backend"
pip install -r requirements.txt
```

**Key packages installed:**
- fastapi - Web framework
- uvicorn - ASGI server
- pandas - Data processing
- numpy - Numerical computing
- pillow - Image processing
- scikit-learn - ML metrics
- plotly - Visualization

### **Step 2: Start Backend Server**

```bash
cd "d:\Minor Project\Astrea-Fairness\Backend"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ **Backend will be running at:** `http://127.0.0.1:8000`

You should see:
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### **Step 3: Start Frontend (In a New Terminal)**

```bash
cd "d:\Minor Project\Astrea-Fairness\Frontend"
streamlit run app.py
```

✅ **Frontend will open at:** `http://localhost:8501`

---

## **🎯 How to Use the Platform**

### **1️⃣ ANALYZING TABULAR DATA (CSV)**

**What it Does:**
- Checks for gender, race, age bias
- Calculates fairness metrics (Demographic Parity, Disparate Impact, etc.)
- Detects if certain groups are treated unfairly
- Generates PDF reports with recommendations

**Steps:**
1. Open frontend at `http://localhost:8501`
2. Select **"Tabular"** data type
3. Upload CSV file
4. Configure (sidebar):
   - **Sensitive Attribute:** Column name for protected characteristic (e.g., "gender")
   - **Ground Truth Column:** Actual outcome (e.g., "hired")
   - **Prediction Column:** Predicted outcome (e.g., "hired")
5. Platform analyzes and shows:
   - 📊 Group distribution
   - 📈 Selection rates by group
   - ⚖️ Fairness metrics
   - 🔍 Bias checks
   - 📋 Recommendations

**Example CSV:**
```
name,gender,age,hired,predicted_hired,salary
John,male,35,1,1,95000
Sarah,female,32,0,0,85000
Michael,male,28,1,1,92000
Emma,female,30,0,0,80000
```

---

### **2️⃣ ANALYZING TEXT DATA**

**What it Does:**
- Detects gender stereotypes in text (e.g., "ambitious" vs "helpful")
- Analyzes race-related biases
- Checks sentiment bias
- Identifies discriminatory language

**Steps:**
1. Select **"Text"** data type
2. Choose upload method:
   - Upload TXT file OR
   - Paste text directly
3. Each line = one text to analyze
4. Click "Analyze Text for Bias"
5. View results:
   - Overall bias score
   - Gender bias analysis
   - Race bias analysis
   - Sentiment patterns

**Example Texts:**
```
The ambitious businessman led the team with authority
The friendly woman helped organize the office schedule
An intelligent engineer solved complex problems
A caring nurse provided excellent patient support
```

---

### **3️⃣ ANALYZING IMAGE DATA**

**What it Does - 8 Analyses:**
1. 👥 **Demographic Representation** - Is one group over/underrepresented?
2. 🌍 **Race/Ethnicity** - Racial diversity detection
3. 👤 **Gender** - Male/female balance
4. 👶 **Age Groups** - Age representation
5. 🎨 **Skin Tone** - Skin tone diversity
6. 🎭 **Pose & Body** - Body position variety
7. 🏞️ **Background** - Professional vs casual settings
8. 😊 **Emotion** - Facial expression patterns

**Steps:**
1. Select **"Image"** data type
2. Upload multiple images (JPG/PNG)
3. Enter demographic labels (one per image):
   ```
   male
   female
   male
   female
   young
   adult
   ```
   You can use any labels: gender, age, race, custom labels, etc.
4. Click "🔍 Analyze Images for Bias"
5. View 9 tabs with detailed analysis:
   - Colors and charts for representation
   - Disparity ratios
   - Bias detection results
   - Diversity scores

**Example Labels:**
- Gender: `male`, `female`, `non-binary`
- Age: `young`, `adult`, `senior`, `child`
- Race: `asian`, `caucasian`, `african`, `hispanic`
- Custom: `employee_A`, `employee_B`, etc.

**Interpreting Results:**
| Score | Level | Action |
|-------|-------|--------|
| 0.0-0.2 | 🟢 Low | Dataset is relatively fair |
| 0.2-0.5 | 🟡 Moderate | Review representation |
| 0.5-0.8 | 🟠 High | Significant bias, mitigate |
| 0.8-1.0 | 🔴 Critical | Urgent action needed |

---

### **4️⃣ ANALYZING MULTIMODAL DATA (Image + Caption Pairs)**

**What it Does:**
- Checks if images and descriptions align properly
- Detects stereotypical language in captions
- Analyzes if groups get different types of descriptions
- Checks caption quality by group

**Steps:**
1. Create CSV with columns:
   - `image_path` - Path to image file
   - `caption` - Text description of image
   - `demographic_group` - Group label

2. Example CSV:
   ```
   image_path,caption,demographic_group
   img_001.jpg,A brilliant engineer solving complex problems,male
   img_002.jpg,A friendly woman helping colleagues,female
   img_003.jpg,A powerful executive making decisions,male
   img_004.jpg,A woman providing support to the team,female
   ```

3. Select **"Multimodal (Image-Caption Pairs)"**
4. Upload CSV
5. Click "Analyze Multimodal Bias"
6. View:
   - 📐 Caption-image alignment
   - 👥 Description consistency across groups
   - 🏷️ Stereotype presence
   - 🔗 Attribute associations

---

## **📊 Understanding Results**

### **Key Metrics**

**Demographic Parity**
- **What:** Equal positive rates across all groups
- **Good Value:** > 0.8
- **Example:** 80% males hired AND 80% females hired

**Disparate Impact**
- **What:** Difference between groups in selection rate
- **Good Value:** < 20% difference
- **Example:** If 80% males hired but only 60% females = 33% disparate impact

**Equal Opportunity**
- **What:** Error rates equal across groups
- **Good Value:** Similar false positive/negative rates

---

## **⚠️ Troubleshooting**

### **Backend not responding?**
```bash
# Make sure backend is running:
cd "d:\Minor Project\Astrea-Fairness\Backend"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### **Frontend won't load?**
```bash
# Make sure Streamlit is installed and running:
cd "d:\Minor Project\Astrea-Fairness\Frontend"
streamlit run app.py
```

### **Image analysis slow?**
- Use smaller images (< 5 MB each)
- Upload fewer images at once (< 20 images)
- PNG format processes faster than JPEG

### **CSV upload error?**
- Ensure column names match exactly (case-sensitive)
- No missing values in key columns
- Save as UTF-8 encoding

---

## **📁 Sample Data Provided**

The platform includes sample datasets:

1. **hiring_candidates.csv** - 20 candidate applications with gender, qualifications, hiring decisions
2. **job_descriptions.csv** - Job posts to check for biased language
3. **gender_stereotype_keywords.csv** - Keywords categorized by stereotype type
4. **demographic_attributes.csv** - Common protected attributes
5. **resume_bias_examples.txt** - 9 detailed resume bias examples
6. **recommendation_letters.csv** - 20 recommendation letters with gendered language
7. **interview_questions.csv** - Interview questions with bias potential
8. **performance_review_language.csv** - 20 performance reviews with biased descriptors
9. **promotion_decisions.csv** - 20 promotion cases showing gender disparity
10. **multimodal_image_captions.csv** - 35 image-caption pairs with stereotypes

### **How to Test:**
1. Use these files to test the platform
2. Upload `hiring_candidates.csv` → Tabular analysis
3. Read sample texts from `resume_bias_examples.txt` → Text analysis
4. Use `recommendation_letters.csv` → See gendered language
5. Use `multimodal_image_captions.csv` → Multimodal analysis

---

## **🔧 Configuration Tips**

### **Sensitive Attribute**
- Most important parameter
- Should be a protected characteristic:
  - `gender` (male, female)
  - `race` (asian, caucasian, african, etc.)
  - `age` (young, adult, senior)
  - `ethnicity`

### **Ground Truth vs Prediction**
- **Ground Truth:** What actually happened (hired=1, not hired=0)
- **Prediction:** What algorithm predicted
- Platform compares these to find bias

### **Column Names**
- Column names are case-sensitive
- No spaces in column names (use underscores: `is_hired` not `is hired`)
- Use exact names from your CSV

---

## **📈 Interpreting Bias Levels**

### **Low Bias (0.0 - 0.2)**
✅ **Status:** Dataset appears fair
- Similar representation across groups
- Similar selection rates
- No extreme discrepancies

### **Moderate Bias (0.2 - 0.5)**
⚠️ **Status:** Some bias detected
- **Action:** Review group distributions
- Investigate why groups differ
- Consider data augmentation

### **High Bias (0.5 - 0.8)**
🔴 **Status:** Significant bias detected
- **Action:** Implement mitigation strategies
- Balance dataset representation
- Remove biased features
- Use fairness-aware algorithms

### **Critical Bias (0.8 - 1.0)**
🚨 **Status:** Severe bias
- **Action:** Stop deployment immediately
- Conduct thorough audit
- Redesign data collection
- Implement strong fairness constraints

---

## **💡 Best Practices**

1. **Start Small** - Test with 50-100 samples first
2. **Use Clear Labels** - Makes results easier to interpret
3. **Check Multiple Attributes** - Analyze gender, race, age separately
4. **Download Reports** - Keep PDF reports for documentation
5. **Understand Your Data** - Know what each column means
6. **Set Baselines** - Test known fair data first
7. **Iterate** - Analyze → Mitigate → Re-analyze

---

## **📞 Support**

If you encounter issues:

1. **Check Terminal Output** - Backend errors show in terminal
2. **Review Frontend Messages** - Red error boxes are helpful
3. **Validate Data** - Ensure CSV follows format
4. **Test Components** - Try text analysis first (simplest)
5. **Restart Services** - Sometimes helps!

---

## **✨ Features Summary**

| Feature | Status | Notes |
|---------|--------|-------|
| Tabular Data Analysis | ✅ Full | All fairness metrics |
| Text Bias Detection | ✅ Full | Gender, race, sentiment |
| Image Analysis (8 types) | ✅ Full | Demographics, race, age, skin tone, pose, background, clothing, emotion |
| Multimodal Analysis | ✅ Full | Caption alignment, stereotype detection |
| PDF Reports | ✅ Full | Download fairness audit reports |
| Recommendations | ✅ Full | Actionable mitigation strategies |
| Real-time Visualization | ✅ Full | Plotly charts and graphs |

---

**Happy Auditing! ⚖️**

For latest updates and documentation, visit the GitHub repository.
