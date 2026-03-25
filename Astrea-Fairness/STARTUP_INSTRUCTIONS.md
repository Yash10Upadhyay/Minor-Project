# 🚀 Quick Startup Guide

## Option 1: Automatic Startup (Easiest)

**Windows PowerShell:**
```powershell
.\START.bat
```

This will:
- ✅ Check dependencies
- ✅ Start Backend (port 8000)
- ✅ Start Frontend (port 8501)
- ✅ Open browser automatically

---

## Option 2: Manual Startup (Separate Terminals)

### Terminal 1: Start Backend
```powershell
.\START-BACKEND.ps1
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Start Frontend
```powershell
.\START-FRONTEND.ps1
```

Wait for: `Local URL: http://localhost:8501`

### Terminal 3: Open Browser
```
http://localhost:8501
```

---

## Option 3: Manual Command-Line Startup

### Terminal 1: Backend
```bash
cd Backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2: Frontend
```bash
cd Frontend
streamlit run app.py --server.port=8501
```

---

## 🛠️ Troubleshooting

### Backend fails to start
```
❌ ERROR: Port 8000 already in use
```
**Solution:** Change port in command or kill process using port 8000
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Frontend can't connect to Backend
```
❌ ERROR: HTTPConnectionError to http://127.0.0.1:8000
```
**Solution:** Make sure Backend is running first with:
```powershell
.\START-BACKEND.ps1
```

### Module not found errors
```
❌ ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Install dependencies
```bash
pip install -r Backend/requirements.txt
```

### Permission Denied on .ps1 files
```
❌ File cannot be loaded because running scripts is disabled
```
**Solution:** Run as Administrator or allow scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 First Test Steps

1. **Tabular Analysis**
   - Upload: `sample_data/hiring_candidates.csv`
   - Column 1 (Label): `Gender`
   - Column 2 (Target): `Hired`
   - View: Fairness metrics and bias analysis

2. **Text Analysis**
   - Input: Paste text or upload from `sample_data/resume_bias_examples.txt`
   - Analyze gender, race, and sentiment bias

3. **Image Analysis**
   - Upload: Any JPG/PNG image
   - Labels: "male"/"female" or any demographic attribute
   - View: 8 dimensions of bias analysis

4. **Multimodal Analysis**
   - Upload: `sample_data/multimodal_image_captions.csv`
   - Select columns for image path, caption, and demographics
   - View: Image-caption alignment and bias patterns

---

## 📖 Documentation

- **Setup Details:** See `SETUP_GUIDE.md`
- **Quick Overview:** See `QUICKSTART.md`
- **Image Analysis Deep Dive:** See `IMAGE_ANALYSIS_GUIDE.md`
- **Implementation Details:** See `IMPLEMENTATION_SUMMARY.md`

---

## ✅ Startup Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r Backend/requirements.txt`)
- [ ] Backend running on http://127.0.0.1:8000
- [ ] Frontend running on http://localhost:8501
- [ ] Browser shows Astrea Fairness interface
- [ ] Sample data folder exists and has CSV files

---

## 🎯 Success Criteria

✅ **Application is working when:**
- Frontend loads without errors
- Can select different data types (Tabular, Text, Image, Multimodal)
- Can upload files and see analysis results
- Visualizations render properly
- No error messages in browser console or terminal

💡 **If stuck:** Check terminal output first - error messages there usually show the exact problem!
