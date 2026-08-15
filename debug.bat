@echo off
cd /d "%~dp0"
title Yatradham SEO Pipeline - DEBUG MODE

echo === DEBUG MODE ===
echo Current folder: %CD%
echo.

echo Checking Python...
python --version 2>&1
py --version 2>&1
echo.

echo Checking venv...
if exist "venv\Scripts\python.exe" (
    echo venv EXISTS
    venv\Scripts\python.exe --version
) else (
    echo venv MISSING
)
echo.

echo Checking .env...
if exist ".env" (echo .env EXISTS) else (echo .env MISSING)
echo.

echo Checking key files...
if exist "main.py" (echo main.py OK) else (echo main.py MISSING!)
if exist "requirements.txt" (echo requirements.txt OK) else (echo requirements.txt MISSING!)
if exist "static\index.html" (echo index.html OK) else (echo index.html MISSING!)
echo.

echo Press any key to run start.bat...
pause >nul
call "%~dp0start.bat"
