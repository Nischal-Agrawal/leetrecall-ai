@echo off
title LeetRecall AI Launcher

cd /d "%~dp0"

echo ==========================================
echo Starting LeetRecall AI...
echo ==========================================
echo.

echo Starting Backend...
start "LeetRecall Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn backend.main:app --reload"

echo.
echo Waiting 10 seconds for backend...
timeout /t 10 /nobreak >nul

echo.
echo Starting Frontend...
start "LeetRecall Frontend" cmd /k "call venv\Scripts\activate.bat && streamlit run frontend/app.py"

echo.
echo Done.
pause