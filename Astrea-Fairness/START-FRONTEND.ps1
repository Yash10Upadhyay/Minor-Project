# ============================================
# Astrea Fairness Platform - Frontend Startup
# ============================================

Write-Host ""
Write-Host "⚖️  Astrea Fairness Platform - Frontend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path "Frontend")) {
    Write-Host "❌ ERROR: Frontend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the Astrea-Fairness directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend folder found" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Checking Streamlit installation..." -ForegroundColor Yellow

$streamlit_installed = pip show streamlit 2>$null

if (-not $streamlit_installed) {
    Write-Host "⚠️  Installing Streamlit..." -ForegroundColor Yellow
    pip install streamlit
} else {
    Write-Host "✅ Streamlit is installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Frontend Server..." -ForegroundColor Green
Write-Host ""
Write-Host "Frontend will start on http://localhost:8501" -ForegroundColor Cyan
Write-Host "Make sure Backend is running on http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting Streamlit..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Push-Location Frontend
Write-Host ""
Write-Host "Running: streamlit run app.py" -ForegroundColor White
Write-Host ""
streamlit run app.py

Pop-Location
