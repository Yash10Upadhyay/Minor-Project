@echo off
REM ============================================
REM Astrea Fairness Platform - Startup Script
REM ============================================

echo.
echo ⚖️  Astrea Fairness Platform Startup
echo ============================================
echo.

REM Check if running from correct directory
if not exist "Backend" (
    echo ❌ ERROR: Backend folder not found!
    echo Please run this script from the Astrea-Fairness directory
    pause
    exit /b 1
)

if not exist "Frontend" (
    echo ❌ ERROR: Frontend folder not found!
    echo Please run this script from the Astrea-Fairness directory
    pause
    exit /b 1
)

echo ✅ Project structure verified

echo.
echo 📦 Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Installing missing dependencies...
    pip install -r Backend\requirements.txt
) else (
    echo ✅ Dependencies are installed
)

echo.
echo 🚀 Starting Astrea Fairness Platform...
echo.
echo Instructions:
echo 1. Backend will start on http://127.0.0.1:8000
echo 2. Frontend will start on http://localhost:8501
echo 3. Open http://localhost:8501 in your browser
echo.
echo Press CTRL+C to stop any service
echo.

echo ============================================
echo Starting Backend Server...
echo ============================================
cd Backend
start "Astrea Backend" cmd /k "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
cd ..

timeout /t 3 /nobreak

echo ============================================
echo Starting Frontend Server...
echo ============================================
cd Frontend
start "Astrea Frontend" cmd /k "streamlit run app.py"
cd ..

echo.
echo ✅ Both servers started!
echo 📖 Check the terminal windows for any errors
echo 🌐 Opening http://localhost:8501 in browser...
timeout /t 3 /nobreak

start "" http://localhost:8501

echo.
echo Platform is starting. Please wait a moment for it to fully load.
pause
