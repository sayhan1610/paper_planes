@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.11.6 or higher.
    pause
    exit /b
)

:: Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

:: Install dependencies
pip install -r requirements.txt

:: Run the game
python brick.py
