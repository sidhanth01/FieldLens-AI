import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
IMAGES_DIR = UPLOADS_DIR / "images"
AUDIO_DIR = UPLOADS_DIR / "audio"

# Ensure required directories exist
for directory in [DATA_DIR, IMAGES_DIR, AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database path
DB_PATH = DATA_DIR / "fieldlens.db"

# Gemini API Key
GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or st.secrets.get("GEMINI_API_KEY", "")
)

if not GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key not found. Please add GEMINI_API_KEY to your .env file."
    )