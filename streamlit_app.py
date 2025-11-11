import streamlit as st
import joblib
from pathlib import Path
import pandas as pd
import re
from typing import Optional, Tuple

ART = Path('artifacts')
PIPELINE_PATH = ART / 'pipeline_lr.joblib'
META_PATH = ART / 'metadata.json'
DEFAULT_COMBINED = Path('combined.csv')
DEFAULT_TRAIN = Path('train.csv')
DEFAULT_TEST = Path('test.csv')

@st.cache_resource
def load_pipeline():
    pipe = joblib.load(PIPELINE_PATH)
    return pipe

@st.cache_resource
def load_meta():
    if META_PATH.exists():
        import json
        with open(META_PATH, 'r') as f:
            return json.load(f)
    return {}

def _clean(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"<br\s*/?>", ' ', s)
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def _guess_columns(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Heuristically find genre, title, artist, and audio columns."""
    cols = {c.lower(): c for c in df.columns}
    # Genre
    genre = None
    for k in ['genre', 'genres', 'label']:
        if k in cols:
            genre = cols[k]
            break
    # Title
    title = None
    for k in ['title', 'song', 'track', 'name']:
        if k in cols:
            title = cols[k]
            break
    # Artist
    artist = None
    for k in ['artist', 'artists', 'singer', 'band']:
        if k in cols:
            artist = cols[k]
            break
    # Audio URL or local path
    audio = None
    for k in ['preview_url', 'audio_url', 'audio', 'url', 'stream_url', 'mp3']:
        if k in cols:
            audio = cols[k]
            break
    return genre, title, artist, audio

@st.cache_data(show_spinner=False)
def load_catalog_from_disk() -> Optional[pd.DataFrame]:
    """Try to load a song catalog from combined.csv(.gz) or train/test."""
    try:
        # Try combined.csv first, then .gz
        if DEFAULT_COMBINED.exists():
            return pd.read_csv(DEFAULT_COMBINED)
        if Path('combined.csv.gz').exists():
            return pd.read_csv('combined.csv.gz', compression='gzip')
        # Fallback to train/test
        parts = []
        if DEFAULT_TRAIN.exists():
            parts.append(pd.read_csv(DEFAULT_TRAIN))
        if DEFAULT_TEST.exists():
            parts.append(pd.read_csv(DEFAULT_TEST))
        if parts:
            return pd.concat(parts, ignore_index=True)
    except Exception as e:
        st.warning(f"Failed to load local catalog: {e}")
    return None

def _render_audio_item(row, title_col, artist_col, audio_col):
    title = str(row.get(title_col, 'Unknown Title')) if title_col else 'Unknown Title'
    artist = str(row.get(artist_col, 'Unknown Artist')) if artist_col else 'Unknown Artist'
    audio = str(row.get(audio_col, '')).strip() if audio_col else ''

    st.markdown(f"**{title}** — {artist}")
    if audio:
        # If local file path exists, play bytes; otherwise assume it's a URL
        p = Path(audio)
        try:
            if p.exists():
                with open(p, 'rb') as f:
                    st.audio(f.read())
            else:
                st.audio(audio)
        except Exception as e:
            st.info(f"Couldn't play audio directly ({e}).")
            search_q = f"{title} {artist}".replace(' ', '%20')
            st.markdown(f"Open in Spotify search: [link](https://open.spotify.com/search/{search_q})")
    else:
        search_q = f"{title} {artist}".replace(' ', '%20')
        st.markdown(f"No audio URL available. Try: [Spotify search](https://open.spotify.com/search/{search_q})")

def show_genre_browser(genre: str, df_catalog: Optional[pd.DataFrame], limit: int = 25):
    st.subheader(f"Songs in predicted genre: {genre}")
    if df_catalog is None or df_catalog.empty:
        st.info("No local catalog found. Upload a CSV with your songs (including a 'Genre' column and optional 'preview_url').")
        uploaded = st.file_uploader('Upload catalog CSV', type=['csv'], key='catalog_upl')
        if uploaded is not None:
            df_catalog = pd.read_csv(uploaded)
        else:
            return

    gcol, tcol, acol, audcol = _guess_columns(df_catalog)
    if not gcol:
        st.error("No genre-like column found in catalog. Add a 'Genre' column and retry.")
        return

    subset = df_catalog[df_catalog[gcol].astype(str) == str(genre)]
    if subset.empty:
        st.warning("No songs found for this genre in the catalog.")
        return

    st.caption(f"Showing up to {limit} of {len(subset)} songs")
    for _, row in subset.head(limit).iterrows():
        _render_audio_item(row, tcol, acol, audcol)
        st.divider()

st.set_page_config(page_title='Lyrics Genre Classifier', page_icon='🎵', layout='wide')
st.title('🎵 Lyrics Genre Classifier')
st.caption('TF-IDF + SVD + Logistic Regression (balanced with undersampling + SMOTE)')

col1, col2 = st.columns([2,1])

with col1:
    mode = st.radio('Prediction mode', ['Single text', 'CSV batch'], horizontal=True)
    if mode == 'Single text':
        text = st.text_area('Paste lyrics text', height=200, placeholder='Enter lyrics here...')
        if st.button('Predict'):
            if not PIPELINE_PATH.exists():
                st.error('Missing artifacts/pipeline_lr.joblib. Please run the notebook cells to generate artifacts.')
            else:
                pipe = load_pipeline()
                pred = pipe.predict([_clean(text)])[0]
                st.success(f'Predicted genre: {pred}')
                # Show catalog and audio players for this genre
                catalog = load_catalog_from_disk()
                show_genre_browser(str(pred), catalog)
    else:
        uploaded = st.file_uploader('Upload CSV with a column named "Lyrics"', type=['csv'])
        if uploaded is not None:
            df = pd.read_csv(uploaded)
            col = st.selectbox('Text column', list(df.columns), index=list(df.columns).index('Lyrics') if 'Lyrics' in df.columns else 0)
            if st.button('Predict for CSV'):
                if not PIPELINE_PATH.exists():
                    st.error('Missing artifacts/pipeline_lr.joblib. Please run the notebook cells to generate artifacts.')
                else:
                    pipe = load_pipeline()
                    preds = pipe.predict(df[col].fillna('').astype(str).map(_clean))
                    out = df.copy()
                    out['pred_genre'] = preds
                    st.dataframe(out.head(50))
                    st.download_button('Download predictions', out.to_csv(index=False).encode('utf-8'), 'predictions.csv', 'text/csv')
                    # Optional: let user browse a specific predicted genre
                    uniq_genres = sorted(pd.Series(preds).unique().tolist())
                    if uniq_genres:
                        st.markdown('---')
                        sel = st.selectbox('Browse songs for predicted genre', uniq_genres)
                        catalog = load_catalog_from_disk()
                        show_genre_browser(str(sel), catalog)

with col2:
    st.subheader('Artifacts status')
    st.write('- Pipeline:', '✅' if PIPELINE_PATH.exists() else '❌', PIPELINE_PATH)
    st.write('- Metadata:', '✅' if META_PATH.exists() else '❌', META_PATH)

    meta = load_meta()
    if meta:
        st.json(meta)
    else:
        st.info('No metadata found. It will be created when you run the training cell in the notebook.')
