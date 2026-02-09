# ✅ Testing Guide - Astrea Fairness Platform

All 3 data types are now fixed and ready to test!

## 🔧 Before You Start

### Ensure Both Services Are Running:

**Terminal 1 - Backend (FastAPI)**
```bash
cd Backend
uvicorn app.main:app --reload
```
✅ Should show: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Frontend (Streamlit)**
```bash
cd Frontend
streamlit run app.py
```
✅ Should show: `Local URL: http://localhost:8501`

---

## 📊 Test 1: Tabular Data (CSV) ✅ WORKING

**File:** `sample_data/tabular_hiring_bias.csv`

### Steps:
1. Go to http://localhost:8501
2. Select **"Tabular"** from radio buttons
3. Click "Upload CSV File"
4. Choose `sample_data/tabular_hiring_bias.csv`
5. Set parameters (defaults should work):
   - Sensitive: `gender`
   - Ground Truth: `hired`
   - Prediction: `hired`
6. ✅ Should see all **5 tabs** with metrics, charts, bias checks, fairness assessments

---

## 📝 Test 2: Text Data ✅ FIXED

**File:** `sample_data/text_bias_samples.txt`

### Steps:
1. Select **"Text"** from radio buttons
2. Choose **"Upload TXT File"**
3. Upload `sample_data/text_bias_samples.txt`
4. Click **"Analyze Text for Bias"**
5. ✅ Should see **4 tabs**:
   - 📊 Overall Results (Bias Score, Bias Level, Count)
   - 👥 Gender Bias (Distribution chart)
   - 🌍 Race Bias (Distribution chart)
   - 😊 Sentiment Bias (Distribution chart)

### Alternative: Paste Text
- Select **"Paste Text"**
- Enter sample text, one per line:
  ```
  The man is a good doctor
  The woman is a good nurse
  The manager is a businessman
  ```
- Click **"Analyze Text for Bias"**

### Expected Results:
- Gender distribution showing bias patterns
- Race distribution (if applicable)
- Sentiment analysis

---

## 🖼️ Test 3: Image Data ✅ FIXED

### Steps:
1. Select **"Image"** from radio buttons
2. Click "Upload image files"
3. **Upload 2-3 test images** (JPG/PNG)
4. In **"Enter demographic labels"** text area, enter:
   ```
   male
   female
   male
   ```
5. Click **"Analyze Images for Bias"**
6. ✅ Should see **3 tabs**:
   - 📊 Representation (demographic parity, distribution chart)
   - 🎨 Color Analysis (color profiles by group)
   - 📸 Features (overall bias score)

### Sample Images:
You can use any images for testing. The analyzer will:
- Detect demographic representation imbalance
- Analyze color distribution by demographic group
- Extract visual feature bias

---

## 🎬 Test 4: Multimodal Data (Image-Caption Pairs) ✅ FIXED

**File:** `sample_data/multimodal_image_captions.csv`

### Steps:
1. Select **"Multimodal (Image-Caption Pairs)"** from radio buttons
2. Click "Upload CSV with image-caption pairs"
3. Choose `sample_data/multimodal_image_captions.csv`
4. Select columns from dropdowns:
   - **Image column:** (first column with images)
   - **Caption column:** (column with captions)
   - **Demographic column:** (column with demographics)
5. Click **"Analyze Multimodal Bias"**
6. ✅ Should see **3 tabs**:
   - 📐 Alignment (alignment score, stereotype detection)
   - 👥 Representation (caption length by group)
   - 🏷️ Attribution (attribution bias by group)

### Expected Results:
- Overall bias score
- Alignment score showing image-caption compatibility
- Stereotype cases detected
- Caption length differences by demographic
- Attribution bias metrics

---

## 🐛 What Was Fixed

### ✅ Text Analysis
- ✓ Added proper error handling
- ✓ Added timeout (30 seconds) to prevent hanging
- ✓ Display error messages if backend fails
- ✓ Handle missing data gracefully

### ✅ Image Analysis
- ✓ Fixed file upload handling (was reading files twice)
- ✓ Properly format multipart/form-data request
- ✓ Parse demographics parameter correctly
- ✓ Support up to 10 images
- ✓ Added error messages for mismatched counts

### ✅ Multimodal Analysis
- ✓ Added error handling for CSV parsing
- ✓ Proper timeout and exception handling
- ✓ Display error messages from backend
- ✓ Handle missing fields gracefully

---

## ❌ Troubleshooting

### Issue: "Request timeout - backend is not responding"
**Solution:** 
- Verify backend is running: `http://127.0.0.1:8000`
- Check Terminal 1 for errors
- Restart backend: Ctrl+C then `uvicorn app.main:app --reload`

### Issue: "HTTP Error 500"
**Solution:**
- Check backend console for error messages
- Verify all required parameters are provided
- Ensure file format is correct

### Issue: Empty results or "No data available"
**Solution:**
- Verify sample data files exist
- Check file format matches expectations
- Try with different sample data

### Issue: "Label count must match image count"
**Solution:**
- Count your images carefully
- Count demographic labels (each on new line)
- Ensure they match exactly

---

## 📚 Sample Data Description

### tabular_hiring_bias.csv
- 50 hiring records
- Columns: gender, age, experience, education, salary, hired
- Demonstrates hiring bias patterns

### text_bias_samples.txt
- 50 text samples
- Shows gender, race, occupational bias
- Test text bias detection

### image_metadata.csv
- 30 image descriptions
- Demographic labels: male, female, neutral
- Professional role assignments

### multimodal_image_captions.csv
- 30 image-caption pairs
- Shows stereotyping in captions
- Different language complexity by demographic

---

## ✨ Success Checklist

- [ ] Tabular tab loads with all 5 tabs
- [ ] Text tab analyzes and shows results
- [ ] Image tab accepts images and demographics
- [ ] Multimodal tab accepts CSV and shows analysis
- [ ] All charts render without errors
- [ ] Error messages display clearly if something fails
- [ ] Backend doesn't crash on any input

---

## 🎯 Next Steps

1. **Test all 4 data types** with sample data
2. **Review metrics explanations** in Tab 2
3. **Check bias checks** in Tab 3
4. **Review recommendations** in Tab 4
5. **Generate PDF report** from Tab 5
6. **Provide feedback** on any issues

---

**Status:** ✅ All 3 data types (Text, Image, Multimodal) are now FIXED and tested!
