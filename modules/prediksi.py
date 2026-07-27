import pandas as pd
import streamlit as st
import re

def preprocessing(teks):
    teks = str(teks).lower()
    teks = re.sub(r"[^a-zA-Z0-9\s]", " ", teks)
    return teks

def prediksi_kamus(teks):
    try:
        kamus = pd.read_csv("kamus_klasifikasi_kejahatan.csv")
    except Exception:
        return None

    teks = preprocessing(teks)

    kamus["kata_kunci"] = kamus["kata_kunci"].astype(str).str.lower().str.strip()
    kamus["label"] = kamus["label"].astype(str).str.strip()

    # cocokkan kata kunci terpanjang terlebih dahulu
    kamus = kamus.sort_values(
        by="kata_kunci",
        key=lambda s: s.str.len(),
        ascending=False
    )

    for _, row in kamus.iterrows():
        if row["kata_kunci"] in teks:
            return row["label"]

    return None

def show():
    st.title("🔍 Prediksi Tingkat Kejahatan (Manual)")

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

        hasil = prediksi_kamus(judul)

        st.subheader("Hasil Prediksi")

        if hasil is None:
            st.error("Jenis perkara tidak ditemukan pada kamus klasifikasi.")
        else:
            st.success(f"Tingkat Kejahatan: {hasil}")
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
