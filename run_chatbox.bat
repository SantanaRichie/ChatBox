@echo off
REM ChatBox Launcher - Run ChatBox from source code
REM No need to open command prompt - just double-click this file!

setlocal enabledelayedexpansion

echo.
echo ====================================
echo    ChatBox - P2P Chat Application
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org
    echo During installation, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

REM Run ChatBox
echo Starting ChatBox...
echo.
python scripts/login.py

pause
