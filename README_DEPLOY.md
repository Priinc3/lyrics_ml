# 🎵 Lyrics Genre Classifier - Standalone App

A self-contained music genre classification app that runs locally without requiring GitHub.

## 📦 What's Included

- **Pre-trained ML model** (TF-IDF + SVD + Logistic Regression)
- **Streamlit UI** for single/batch predictions
- **Song browser** — see all songs of predicted genre with playback
- **No external dependencies** — everything runs locally

## 🚀 Quick Start

### **macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

### **Windows:**
Double-click `run.bat` or run in Command Prompt:
```cmd
run.bat
```

### **Manual Setup (any OS):**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens at **http://localhost:8501**

## 🌐 Share With Others

### **On Same WiFi Network:**
1. Run the app (see Quick Start above)
2. Streamlit shows a "Network URL" — copy it
3. Share that URL with others on the same WiFi
4. They can access your app without installing anything

**Example Network URL:**
```
http://192.168.1.100:8501
```

### **Share the Entire Folder:**
- Zip this `deploy/` folder
- Send to anyone via email/cloud
- They extract it and run `run.sh` (macOS/Linux) or `run.bat` (Windows)
- No GitHub, no internet required (except for optional Spotify search links)

## 📝 How to Use

### **Single Prediction:**
1. Paste song lyrics
2. Click "Predict"
3. See predicted genre + all songs in that genre with playback

### **Batch Prediction:**
1. Upload a CSV with a "Lyrics" column
2. Click "Predict for CSV"
3. Download results + browse by predicted genre

### **Add Your Own Songs:**
Place `combined.csv` or `combined.csv.gz` in the same folder as `streamlit_app.py`. Must include:
- `Genre` column (any genre names)
- `Title`/`Song`/`Track` (song name)
- `Artist` (artist name)
- `preview_url`/`audio_url` (optional, for playback)

## ⚙️ Requirements

- **Python 3.8+** (free from python.org)
- **Internet** (first run only, to install dependencies)

## 📂 File Structure

```
deploy/
├── run.sh                          # macOS/Linux launcher
├── run.bat                         # Windows launcher
├── streamlit_app.py                # Main app
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── artifacts/
    ├── pipeline_lr.joblib          # Trained model pipeline
    ├── svd_200.joblib              # Dimensionality reducer
    └── tfidf_vectorizer.joblib     # Text vectorizer
```

## 🎯 Features

✅ **Predict genres** from song lyrics  
✅ **Browse songs** by predicted genre  
✅ **Play audio** (via URL or local file)  
✅ **Batch predictions** (upload CSV, download results)  
✅ **Works offline** (except Spotify search links)  
✅ **No GitHub/account** required  
✅ **Shareable** — send folder to anyone  

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Download from python.org and install (add to PATH) |
| Port 8501 already in use | Run: `streamlit run streamlit_app.py --server.port 8502` |
| Dependencies fail to install | Ensure Python 3.8+, try: `pip install --upgrade pip` first |
| Can't see Network URL | Make sure you're on the same WiFi; check firewall settings |

## 📜 License

Internal learning project — use and modify as needed.

---

**Enjoy classifying genres!** 🎶
