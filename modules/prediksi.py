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
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


def show():
    st.title("🔍 Prediksi Tingkat Kejahatan")

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

        if vectorizer is None:
            st.error(
                "Vectorizer tidak ditemukan di session. "
                "Jika Anda memakai TF-IDF manual, sesuaikan bagian prediksi "
                "agar membentuk vektor fitur manual yang sama seperti saat training."
            )
            return

        X = vectorizer.transform([hasil_pre])

        prediksi = model.predict(X)[0]
        probabilitas = model.predict_proba(X)[0]

        st.subheader("Hasil Prediksi")
        st.success(f"Tingkat Kejahatan: {prediksi}")

        st.info("Prediksi dilakukan menggunakan model Naïve Bayes yang telah dilatih dari dataset. Judul tidak harus sama dengan data latih; model memprediksi berdasarkan pola kata yang dipelajari.")

        prob_df = pd.DataFrame({
            "Kelas": model.classes_,
            "Probabilitas": [round(p*100,2) for p in probabilitas]
        })

        prob_df["Probabilitas (%)"]=prob_df.pop("Probabilitas")

        st.subheader("Probabilitas Prediksi")
        st.dataframe(prob_df,use_container_width=True)

        tingkat_keyakinan=max(probabilitas)
        if tingkat_keyakinan<0.60:
            st.warning("Keyakinan model rendah karena input memiliki pola yang kurang mirip dengan data latih.")
        else:
            st.success(f"Keyakinan model: {tingkat_keyakinan*100:.2f}%")

        csv=prob_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Hasil Prediksi",csv,file_name="hasil_prediksi.csv",mime="text/csv")

