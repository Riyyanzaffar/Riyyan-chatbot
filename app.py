import base64
from pathlib import Path

import streamlit as st

from backend.rag import answer_question
from backend.config import APP_TITLE
from backend.vector_store import index_exists, build_index
from backend.loader import load_documents
from backend.chunker import chunk_documents
from backend.config import DATA_DIR

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
BOT_NAME = "Riyyan Zaffar Chat Bot"
TAGLINE = "Your personal AI assistant, powered by a custom knowledge base"

LOGO_CANDIDATES = [
    "assets/logo.png",
    "assets/logo.jpg",
    "assets/logo.jpeg",
    "assets/logo.webp",
]


def find_logo():
    for candidate in LOGO_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path
    return None


def logo_to_base64(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    if path.suffix.lower() == ".webp":
        mime = "image/webp"
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def make_logo_from_photo():
    """If you put your portrait as photo.jpg / photo.png / photo.jpeg next to app.py,
    this crops it into a small square logo at assets/logo.png (done once)."""
    from PIL import Image

    for name in ("photo.jpg", "photo.jpeg", "photo.png", "photo.webp"):
        photo = Path(name)
        if photo.exists():
            img = Image.open(photo).convert("RGB")
            w, h = img.size
            size = int(min(w, h) * 0.78)
            left = (w - size) // 2
            top = int(h * 0.03)
            img = img.crop((left, top, left + size, top + size))
            img = img.resize((256, 256), Image.LANCZOS)
            Path("assets").mkdir(exist_ok=True)
            img.save("assets/logo.png", optimize=True)
            return


if find_logo() is None:
    try:
        make_logo_from_photo()
    except Exception:
        pass

LOGO_PATH = find_logo()

st.set_page_config(
    page_title=BOT_NAME,
    page_icon=str(LOGO_PATH) if LOGO_PATH else "💬",
    layout="centered",
)

# ----------------------------------------------------------------------------
# Prepare knowledge base on first cloud startup
# ----------------------------------------------------------------------------
if not index_exists():
    with st.spinner("Preparing knowledge base... This may take a few minutes."):
        documents = load_documents(DATA_DIR)
        if not documents:
            st.error("No knowledge-base documents found in backend/data/.")
            st.stop()

        chunks = chunk_documents(documents)
        if not chunks:
            st.error("No text chunks were created from the knowledge base.")
            st.stop()

        build_index(chunks)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Background */
    .stApp {
        background:
            radial-gradient(900px 500px at 10% -10%, rgba(99,102,241,0.25), transparent 60%),
            radial-gradient(800px 500px at 100% 0%, rgba(236,72,153,0.18), transparent 60%),
            linear-gradient(180deg, #0b0f1a 0%, #0d1220 100%);
        color: #e5e7eb;
    }

    /* Hide default chrome */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

    .block-container { padding-top: 2rem; max-width: 820px; }

    /* Hero header */
    .hero {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 20px 24px;
        margin-bottom: 18px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.10);
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    }
    .hero img, .hero .logo-fallback {
        width: 72px; height: 72px;
        border-radius: 50%;
        object-fit: cover;
        object-position: center top;
        border: 2px solid transparent;
        background:
            linear-gradient(#0b0f1a, #0b0f1a) padding-box,
            linear-gradient(135deg, #6366f1, #ec4899) border-box;
        box-shadow: 0 0 24px rgba(99,102,241,0.55);
        flex-shrink: 0;
    }
    .hero .logo-fallback {
        display: flex; align-items: center; justify-content: center;
        font-size: 32px;
    }
    .hero h1 {
        margin: 0;
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #ffffff, #a5b4fc 55%, #f9a8d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p { margin: 4px 0 0; color: #9ca3af; font-size: 0.92rem; }
    .status {
        display: inline-flex; align-items: center; gap: 6px;
        margin-top: 8px; font-size: 0.75rem; color: #86efac;
    }
    .status .dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #22c55e; box-shadow: 0 0 10px #22c55e;
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse { 0%,100% {opacity: 1;} 50% {opacity: .35;} }

    /* Welcome card */
    .welcome {
        text-align: center;
        padding: 34px 20px;
        margin: 10px 0 20px;
        border-radius: 20px;
        border: 1px dashed rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.03);
        color: #cbd5e1;
    }
    .welcome h3 { margin: 0 0 6px; color: #fff; font-weight: 600; }
    .welcome span { color: #94a3b8; font-size: 0.93rem; }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        animation: fadeUp .35s ease;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(236,72,153,0.14));
        border-color: rgba(129,140,248,0.35);
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Sources expander */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
    }

    /* Global text colours (fixes invisible text) */
    .stApp, .stApp p, .stApp li, .stApp span, .stApp label,
    .stApp div[data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] * {
        color: #e5e7eb;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: #ffffff; }
    .hero h1 { -webkit-text-fill-color: transparent; color: transparent; }
    .hero p { color: #9ca3af; }
    .status, .status * { color: #86efac; }
    .welcome h3 { color: #ffffff; }
    .welcome span { color: #94a3b8; }
    .footer-note { color: #6b7280; }

    /* Chat input */
    [data-testid="stBottom"], [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb="textarea"],
    [data-testid="stChatInput"] div[data-baseweb="base-input"] {
        background: #111827 !important;
        border-radius: 18px;
    }
    [data-testid="stChatInput"] {
        border: 1px solid rgba(129,140,248,0.5);
        box-shadow: 0 0 24px rgba(99,102,241,0.25);
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #a5b4fc;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
        -webkit-text-fill-color: #9ca3af !important;
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #6366f1, #ec4899) !important;
        color: #ffffff !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * { color: #e5e7eb !important; }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    section[data-testid="stSidebar"] small { color: #9ca3af !important; }
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * { color: #ffffff !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10,14,26,0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        background: linear-gradient(135deg, #6366f1, #ec4899);
        color: white;
        font-weight: 600;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 22px rgba(99,102,241,0.45);
        border-color: transparent;
        color: white;
    }

    .footer-note {
        text-align: center; color: #6b7280; font-size: 0.75rem; margin-top: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
if LOGO_PATH:
    logo_html = f'<img src="{logo_to_base64(LOGO_PATH)}" alt="logo" />'
else:
    logo_html = '<div class="logo-fallback">🤖</div>'

st.markdown(
    f"""
    <div class="hero">
        {logo_html}
        <div>
            <h1>{BOT_NAME}</h1>
            <p>{TAGLINE}</p>
            <div class="status"><span class="dot"></span> Online &middot; Ready to help</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    if LOGO_PATH:
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown(f"### {BOT_NAME}")
    st.caption("Ask anything from the knowledge base. Answers include their sources.")
    st.divider()
    if st.button("🗑️  Clear conversation"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Built by Riyyan Zaffar")

# ----------------------------------------------------------------------------
# Chat state
# ----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

BOT_AVATAR = str(LOGO_PATH) if LOGO_PATH else "🤖"
USER_AVATAR = "🧑"

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome">
            <h3>👋 Hello, how can I help you today?</h3>
            <span>Type a question below and I'll search the knowledge base for you.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    avatar = BOT_AVATAR if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(source)

# ----------------------------------------------------------------------------
# Input / answer
# ----------------------------------------------------------------------------
question = st.chat_input("Type your question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(question)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            result = answer_question(question)
        st.markdown(result["answer"])

        sources = result.get("sources") or []
        if sources:
            with st.expander("📚 Sources"):
                for source in sources:
                    st.write(source)

    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"], "sources": sources}
    )

st.markdown(
    f'<div class="footer-note">© {BOT_NAME} &middot; Built with Streamlit</div>',
    unsafe_allow_html=True,
)