import pandas as pd
import streamlit as st
import joblib
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocessing(teks):
    teks = str(teks).lower()
    teks = re.sub(r"[^a-zA-Z0-9\s]", " ", teks)
    teks = " ".join(stemmer.stem(k) for k in teks.split())
    return teks

def show():
    st.title("🔍 Prediksi Tingkat Kejahatan (Naïve Bayes)")

    try:
        model = joblib.load("model/model_nb.pkl")
        vectorizer = joblib.load("model/tfidf.pkl")
    except Exception:
        st.error("Model atau TF-IDF belum tersedia. Jalankan menu Klasifikasi terlebih dahulu.")
        return

    judul = st.text_area(
        "Judul Berita",
        height=120,
        placeholder="Contoh: Polisi menangkap pelaku pembunuhan..."
    )

    if "riwayat_prediksi" not in st.session_state:
        st.session_state["riwayat_prediksi"] = []

    if st.button("Prediksi"):
        if not judul.strip():
            st.warning("Masukkan judul berita terlebih dahulu.")
            return

        teks = preprocessing(judul)
        X = vectorizer.transform([teks])

        hasil = model.predict(X)[0]
        probabilitas = model.predict_proba(X)[0]

        st.subheader("Hasil Prediksi")
        st.success(f"Tingkat Kejahatan: {hasil}")

        prob_df = pd.DataFrame({
            "Kelas": model.classes_,
            "Probabilitas": probabilitas
        })
        st.dataframe(prob_df, use_container_width=True)

        st.session_state["riwayat_prediksi"].append({
            "Judul": judul,
            "Kategori": hasil
        })

    if st.session_state["riwayat_prediksi"]:
        st.subheader("Riwayat Prediksi")
        riwayat = pd.DataFrame(st.session_state["riwayat_prediksi"])
        st.dataframe(riwayat, use_container_width=True)

        csv = riwayat.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Hasil Prediksi",
            csv,
            file_name="riwayat_prediksi.csv",
            mime="text/csv"
        )

        if st.button("🔁 Repeat"):
            st.session_state["riwayat_prediksi"] = []
            st.rerun()
