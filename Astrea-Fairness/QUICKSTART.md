# 🎯 Quick Start Guide - Astrea Fairness Platform

## **In 5 Minutes**

### **1. Start Backend** (Terminal 1)
```bash
cd "d:\Minor Project\Astrea-Fairness\Backend"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### **2. Start Frontend** (Terminal 2)
```bash
cd "d:\Minor Project\Astrea-Fairness\Frontend"
streamlit run app.py
```

### **3. Open Browser**
```
http://localhost:8501
```

---

## **Quick Test- Use Sample Data**

### **Test 1: Tabular Data (1 min)**
1. Select "Tabular" 
2. Upload: `sample_data/hiring_candidates.csv`
3. Settings:
   - Sensitive: `gender`
   - Ground Truth: `hired`
   - Prediction: `hired`
4. ✅ See bias in hiring decisions

### **Test 2: Text Analysis (1 min)**
1. Select "Text"
2. Paste this:
```
The brilliant engineer solved complex problems
The friendly woman helped organize the team
```
3. ✅ See gender bias in language

### **Test 3: Multimodal (1 min)**
1. Select "Multimodal (Image-Caption Pairs)"
2. Upload: `sample_data/multimodal_image_captions.csv`
3. Select columns:
   - Image: `image_path`
   - Caption: `caption`
   - Demographic: `demographic_group`
4. ✅ See stereotype detection in captions

### **Test 4: Image Analysis (2 min)**
1. Select "Image"
2. Upload 3-5 JPG/PNG images
3. Add labels:
```
male
female
male
female
```
4. ✅ See 8 different bias analyses

---

## **🔑 Key Shortcuts**

| Action | File |
|--------|------|
| View all metrics | [METRICS_GUIDE.md](METRICS_GUIDE.md) |
| See feature summary | [FEATURES_SUMMARY.md](FEATURES_SUMMARY.md) |
| Full setup guide | [SETUP_GUIDE.md](SETUP_GUIDE.md) |
| Sample data | `sample_data/` folder |
| Backend code | `Backend/app/` |
| Frontend code | `Frontend/app.py` |

---

## **🎛️ Configuration (Sidebar)**

```
Sensitive Attribute: gender
Ground Truth Column: hired
Prediction Column: hired
```

Change these for different analysis!

---

## **📊 Understanding Scores**

```
🟢 0.0-0.2  = Low Bias (Fair)
🟡 0.2-0.5  = Moderate Bias (Review)
🟠 0.5-0.8  = High Bias (Mitigate)
🔴 0.8-1.0  = Critical Bias (Stop!)
```

---

## **⚡ Common Issues**

| Issue | Fix |
|-------|-----|
| Backend won't start | Check port 8000 not in use |
| Frontend won't load | Ensure backend is running |
| File upload fails | Check CSV format, column names |
| Images not analyzing | Use JPG/PNG max 5MB each |

---

## **🎯 Best Use Cases**

1. **HR Teams** → Analyze hiring data for gender/race bias
2. **Marketing** → Check image diversity in campaigns
3. **ML Engineers** → Validate model fairness before deployment
4. **Researchers** → Audit datasets for bias
5. **Compliance** → Generate fairness reports

---

**Ready? Open http://localhost:8501 and start auditing!**

For detailed help, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

