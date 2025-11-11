#!/bin/bash

# Lyrics Genre Classifier - Local Runner
# This script sets up and runs the Streamlit app locally

set -e

echo "🎵 Lyrics Genre Classifier - Local Setup"
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade pip
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Run Streamlit app
echo ""
echo "✅ Setup complete!"
echo "🚀 Starting Streamlit app..."
echo ""
echo "   Local URL:     http://localhost:8501"
echo "   Share on LAN:  Share the Network URL with others on your WiFi"
echo ""
streamlit run streamlit_app.py
