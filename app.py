import streamlit as st
from pathlib import Path

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

load_css()


# ==============================
# SIDEBAR
# ==============================

st.sidebar.image(
    "asset/logo_polri.jpg",
    width=80
)
st.sidebar.header("KLASIFIKASI")
st.sidebar.caption("TINGKAT KEJAHATAN")

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

# ==============================
# ROUTING
# ==============================

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
