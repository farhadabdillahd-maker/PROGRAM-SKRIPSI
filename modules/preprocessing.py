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
# KAMUS NORMALISASI
# ==============================

normalization_dict = {
    "yg": "yang",
    "dgn": "dengan",
    "tdk": "tidak",
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "ngga": "tidak",
    "krn": "karena",
    "karna": "karena",
    "utk": "untuk",
    "dr": "dari",
    "dri": "dari",
    "org": "orang",
    "sbg": "sebagai",
    "dlm": "dalam",
    "thd": "terhadap",
    "pd": "pada",
    "tsb": "tersebut",
    "dll": "dan lain-lain",
    "dsb": "dan sebagainya",
    "bbrp": "beberapa",
    "blm": "belum",
    "sdh": "sudah",
    "udh": "sudah",
    "adlh": "adalah",
    "krg": "kurang",
    "lebih": "lebih",
}

def normalisasi(tokens):
    return [normalization_dict.get(word, word) for word in tokens]


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
        progress.progress(20)

        # Tokenizing
        df["Tokenizing"] = df["Case Folding"].apply(tokenizing)
        progress.progress(40)

        # Stopword Removal
        df["Stopword Removal"] = df["Tokenizing"].apply(stopword_removal)
        progress.progress(60)

        # Stemming
        df["Stemming"] = df["Stopword Removal"].apply(stemming)
        progress.progress(80)

        # Normalisasi (tahap terakhir)
        df["Normalisasi"] = df["Stemming"].apply(normalisasi)
        progress.progress(100)

        # Final Text
        df["Final Text"] = df["Normalisasi"].apply(lambda x: " ".join(x))

        # Auto Label berdasarkan Jenis Perkara
        try:
            kamus = pd.read_csv("kamus_klasifikasi_kejahatan.csv")
        except FileNotFoundError:
            try:
                kamus = pd.read_csv("kamus_klasifikasi_kejahatan.csv")
            except FileNotFoundError:
                kamus = None

        if kamus is not None:
            # Sesuaikan nama kolom kamus
            kolom_jenis = None
            for c in ["Jenis Perkara","jenis_perkara","jenis perkara","kata_kunci"]:
                if c in kamus.columns:
                    kolom_jenis = c
                    break

            kolom_label = None
            for c in ["Pelabelan","Label","label","kategori"]:
                if c in kamus.columns:
                    kolom_label = c
                    break

            if kolom_jenis and kolom_label and "Jenis Perkara" in df.columns:
                kamus[kolom_jenis] = kamus[kolom_jenis].astype(str).str.strip().str.lower()
                kamus[kolom_label] = kamus[kolom_label].astype(str).str.strip()

                kamus_dict = dict(zip(kamus[kolom_jenis], kamus[kolom_label]))

                df["Pelabelan"] = (
                    df["Jenis Perkara"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .map(kamus_dict)
                )

                df["Pelabelan"] = df["Pelabelan"].fillna("Belum Ada Label")
            else:
                st.error("Kolom kamus tidak sesuai.")
                df["Pelabelan"] = "Belum Ada Label"
        else:
            st.error("File kamus tidak ditemukan.")
            df["Pelabelan"] = "Belum Ada Label"

        progress.progress(100)

        # Simpan hasil preprocessing
        st.session_state["preprocessed"] = df

        st.success("✅ Preprocessing berhasil.")

        # ==============================
        # HASIL PELABELAN
        # ==============================
        st.subheader("Hasil Pelabelan")

        # Tampilkan hasil pelabelan terlebih dahulu
        kolom_label = []

        if "No" in df.columns:
            kolom_label.append("No")
        if "Jenis Perkara" in df.columns:
            kolom_label.append("Jenis Perkara")

        kolom_label.extend([
            "Judul Media Nasional",
            "Pelabelan"
        ])

        st.dataframe(
            df[kolom_label],
            use_container_width=True
        )

        # ==============================
        # HASIL PREPROCESSING
        # ==============================
        st.subheader("Hasil Preprocessing")

        st.dataframe(
            df[
                [
                    "Judul Media Nasional",
                    "Case Folding",
                    "Tokenizing",
                    "Stopword Removal",
                    "Stemming",
                    "Normalisasi",
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
