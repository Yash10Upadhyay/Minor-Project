# ============================================
# Astrea Fairness Platform - Startup Script
# ============================================

Write-Host ""
Write-Host "⚖️  Astrea Fairness Platform Startup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path "Backend")) {
    Write-Host "❌ ERROR: Backend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the Astrea-Fairness directory" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "Frontend")) {
    Write-Host "❌ ERROR: Frontend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the Astrea-Fairness directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Project structure verified" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow

$fastapi_installed = pip show fastapi 2>$null

if (-not $fastapi_installed) {
    Write-Host "⚠️  Installing missing dependencies..." -ForegroundColor Yellow
    pip install -r Backend\requirements.txt
} else {
    Write-Host "✅ Dependencies are installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Astrea Fairness Platform..." -ForegroundColor Green
Write-Host ""
Write-Host "Instructions:" -ForegroundColor Cyan
Write-Host "1. Backend will start on http://127.0.0.1:8000" -ForegroundColor White
Write-Host "2. Frontend will start on http://localhost:8501" -ForegroundColor White
Write-Host "3. Open http://localhost:8501 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop any service" -ForegroundColor Yellow
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Terminal 1: Starting Backend Server..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Push-Location Backend
Write-Host ""
Write-Host "Running: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000" -ForegroundColor White
Write-Host ""
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Pop-Location
