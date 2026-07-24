import re
import joblib
import pandas as pd
import streamlit as st
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_words = set(stopwords.words("indonesian"))


def preprocessing(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


# ==========================================
# PREDIKSI MANUAL BERDASARKAN KAMUS
# ==========================================

def prediksi_kamus(text):
    try:
        kamus = pd.read_csv("kamus_kejahatan.csv")

        kamus["kata_kunci"] = (
            kamus["kata_kunci"]
            .astype(str)
            .str.lower()
        )

        text = text.lower()

        # Prioritas kata terpanjang agar lebih akurat
        kamus = kamus.sort_values(
            by="kata_kunci",
            key=lambda x: x.str.len(),
            ascending=False
        )

        for _, row in kamus.iterrows():
            if row["kata_kunci"] in text:
                return row["kategori"]

    except Exception:
        pass

    return None


def show():

    st.title("🔍 Prediksi Tingkat Kejahatan")

    # Load model
    if "model" in st.session_state:
        model = st.session_state["model"]
    else:
        try:
            model = joblib.load("model/model_nb.pkl")
        except Exception:
            st.error("Model belum tersedia. Jalankan menu Klasifikasi terlebih dahulu.")
            return

    vectorizer = st.session_state.get("vectorizer", None)

    st.write("Masukkan judul berita untuk diprediksi.")

    judul = st.text_area(
        "Judul Berita",
        height=120,
        placeholder="Contoh: Polisi menangkap pelaku pencurian sepeda motor..."
    )

    if st.button("Prediksi"):

        if not judul.strip():
            st.warning("Masukkan judul berita terlebih dahulu.")
            return

        hasil_pre = preprocessing(judul)

        st.subheader("Hasil Preprocessing")
        st.write(hasil_pre)


        # Cek kamus terlebih dahulu
        hasil_kamus = prediksi_kamus(hasil_pre)


        if hasil_kamus:

            prediksi = hasil_kamus

            st.subheader("Hasil Prediksi")
            st.success(
                f"Tingkat Kejahatan: {prediksi} (berdasarkan kamus)"
            )

            prob_df = pd.DataFrame({
                "Kelas": [prediksi],
                "Probabilitas": [100]
            })

        else:

            if vectorizer is None:
                st.error(
                    "Vectorizer tidak ditemukan. "
                    "Silakan jalankan TF-IDF terlebih dahulu."
                )
                return

            X = vectorizer.transform([hasil_pre])

            prediksi = model.predict(X)[0]
            probabilitas = model.predict_proba(X)[0]

            st.subheader("Hasil Prediksi")
            st.success(
                f"Tingkat Kejahatan: {prediksi} (berdasarkan Naïve Bayes)"
            )

            prob_df = pd.DataFrame({
                "Kelas": model.classes_,
                "Probabilitas": probabilitas
            })


        st.subheader("Probabilitas")
        st.dataframe(prob_df, use_container_width=True)

        csv = prob_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Probabilitas",
            csv,
            file_name="hasil_prediksi.csv",
            mime="text/csv"
        )
