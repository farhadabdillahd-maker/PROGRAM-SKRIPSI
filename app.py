import streamlit as st

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

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stSidebar"]{
background:#0B1F3A;
}

[data-testid="stSidebar"] *{
color:white;
}

.block-container{
padding-top:1rem;
padding-bottom:1rem;
}

.stButton>button{
width:100%;
border-radius:10px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🛡️")
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
