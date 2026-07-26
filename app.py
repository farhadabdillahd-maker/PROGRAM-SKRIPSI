import streamlit as st
from pathlib import Path
import base64

# ==============================
# KONFIGURASI HALAMAN
# ==============================

st.set_page_config(
    page_title="Klasifikasi Tingkat Kejahatan",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# IMPORT MODULE
# ==============================

from modules import (
    home,
    upload_dataset,
    preprocessing,
    tfidf,
    klasifikasi,
    prediksi,
    about
)

# ==============================
# CSS
# ==============================

def load_css():
    css_path = Path(__file__).parent / "asset" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS tidak ditemukan: {css_path}")

def set_gif_background():
    gif_path = Path(__file__).parent / "asset" / "latar.gif"
    if gif_path.exists():
        gif = base64.b64encode(gif_path.read_bytes()).decode()
        st.markdown(f'''
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(255,255,255,0.30), rgba(255,255,255,0.30)),
                url("data:image/gif;base64,{gif}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        ''', unsafe_allow_html=True)

load_css()
set_gif_background()

# ==============================
# SIDEBAR
# ==============================

def logo_base64():
    logo_path = Path(__file__).parent / "asset" / "logo_polri.png"
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.sidebar.markdown(f"""
<div style="text-align:center; margin-top:10px; margin-bottom:20px;">
    <img src="data:image/png;base64,{logo_base64()}" width="90">
    <h2 style="color:white; margin:10px 0 0 0; font-weight:800;">KLASIFIKASI</h2>
    <div style="color:#B8C2D9; font-size:16px; font-weight:600;">TINGKAT KEJAHATAN</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "📂 Upload Dataset",
        "🧹 Preprocessing",
        "📝 TF-IDF",
        "🤖 Klasifikasi",
        "🔍 Prediksi",
        "ℹ️ About"
    ]
)

if menu == "🏠 Home":
    home.show()
elif menu == "📂 Upload Dataset":
    upload_dataset.show()
elif menu == "🧹 Preprocessing":
    preprocessing.show()
elif menu == "📝 TF-IDF":
    tfidf.show()
elif menu == "🤖 Klasifikasi":
    klasifikasi.show()
elif menu == "🔍 Prediksi":
    prediksi.show()
elif menu == "ℹ️ About":
    about.show()
