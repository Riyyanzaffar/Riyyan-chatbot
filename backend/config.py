import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Local development reads .env; Streamlit Cloud reads st.secrets.
try:
    import streamlit as st
    STREAMLIT_SECRETS = st.secrets
except Exception:
    STREAMLIT_SECRETS = {}

APP_TITLE = os.getenv("APP_TITLE", "RAG Chatbot")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or STREAMLIT_SECRETS.get("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL") or STREAMLIT_SECRETS.get(
    "GROQ_MODEL", "openai/gpt-oss-20b"
)

DATA_DIR = ROOT_DIR / "backend" / "data"
VECTOR_DIR = ROOT_DIR / "backend" / "vector_db"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "4"))

