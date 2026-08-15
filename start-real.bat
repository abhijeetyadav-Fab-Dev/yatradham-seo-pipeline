@echo off
cd /d "%~dp0"
title Yatradham SEO Pipeline - Live Mode

echo ==========================================
echo  Yatradham SEO Pipeline - One-Click Setup
echo ==========================================
echo.

:: Check .env
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Step 1: Rename .env.example to .env
    echo Step 2: Open .env and paste your OpenRouter API key
    echo Step 3: Double-click start-real.bat again
    echo.
    pause
    exit /b 1
)

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ from python.org
echo Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

:: Create venv if missing
if not exist "venv\Scripts\python.exe" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
) else (
    echo [1/4] Virtual environment already exists.
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies if missing
venv\Scripts\python.exe -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [2/4] Installing dependencies ^(first time only^)...
    venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo [2/4] Dependencies already installed.
)

:: Set mode
set DRY_RUN=false
echo [3/4] Mode: LIVE AI ^(Nemotron^)

:: Open browser
echo [4/4] Opening dashboard...
start "" "http://localhost:8000/static/index.html"

:: Start server
echo.
echo ==========================================
echo  SERVER IS RUNNING
echo  Dashboard: http://localhost:8000/static/index.html
echo  Press Ctrl+C to stop
echo ==========================================
echo.

venv\Scripts\python.exe main.py

:: Keep window open after server stops
echo.
echo Server stopped. Press any key to close...
pause >nul
