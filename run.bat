@echo off
REM Lyrics Genre Classifier - Local Runner (Windows)

echo.
echo 🎵 Lyrics Genre Classifier - Local Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install --upgrade pip -q
pip install -r requirements.txt -q

REM Run Streamlit app
echo.
echo ✅ Setup complete!
echo 🚀 Starting Streamlit app...
echo.
echo    Local URL:     http://localhost:8501
echo    Share on LAN:  Share the Network URL with others on your WiFi
echo.
streamlit run streamlit_app.py

pause
