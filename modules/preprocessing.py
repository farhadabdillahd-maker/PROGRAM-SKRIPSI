import streamlit as st
import pandas as pd
import nltk

from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Download stopword jika belum ada
try:
    stopwords.words("indonesian")
except LookupError:
    nltk.download("stopwords")

# Inisialisasi stemmer dan stopword
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_words = set(stopwords.words("indonesian"))


# ==============================
# FUNGSI PREPROCESSING
# ==============================

def case_folding(text):
    return str(text).lower()


def tokenizing(text):
    return text.split()


def stopword_removal(tokens):
    return [word for word in tokens if word not in stop_words]


def stemming(tokens):
    return [stemmer.stem(word) for word in tokens]


# ==============================
# HALAMAN PREPROCESSING
# ==============================

def show():

    st.title("🧹 Preprocessing")

    if "dataset" not in st.session_state:
        st.warning("Silakan upload dataset terlebih dahulu.")
        return

    df = st.session_state["dataset"].copy()

    if "Judul Media Nasional" not in df.columns:
        st.error("Kolom 'Judul Media Nasional' tidak ditemukan.")
        return

    if st.button("Mulai Preprocessing"):

        progress = st.progress(0)

        # Case Folding
        df["Case Folding"] = df["Judul Media Nasional"].apply(case_folding)
        progress.progress(25)

        # Tokenizing
        df["Tokenizing"] = df["Case Folding"].apply(tokenizing)
        progress.progress(50)

        # Stopword Removal
        df["Stopword Removal"] = df["Tokenizing"].apply(stopword_removal)
        progress.progress(75)

        # Stemming
        df["Stemming"] = df["Stopword Removal"].apply(stemming)

        # Final Text
        df["Final Text"] = df["Stemming"].apply(lambda x: " ".join(x))

        progress.progress(100)

        # Simpan hasil preprocessing
        st.session_state["preprocessed"] = df

        st.success("✅ Preprocessing berhasil.")

        st.subheader("Hasil Preprocessing")

        st.dataframe(
            df[
                [
                    "Judul Media Nasional",
                    "Case Folding",
                    "Tokenizing",
                    "Stopword Removal",
                    "Stemming",
                    "Final Text",
                ]
            ],
            use_container_width=True,
        )

        # Ringkasan
        st.subheader("Ringkasan")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Jumlah Dokumen", len(df))

        with col2:
            total_kata = df["Final Text"].apply(lambda x: len(x.split())).sum()
            st.metric("Jumlah Kata", total_kata)
