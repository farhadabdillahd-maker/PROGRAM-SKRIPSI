import pandas as pd
import streamlit as st


# ==========================================
# PREDIKSI MANUAL BERDASARKAN KAMUS KEJAHATAN
# ==========================================

def prediksi_kamus(text):

    try:
        kamus = pd.read_csv("kamus_kejahatan.csv")

        kamus["kata_kunci"] = (
            kamus["kata_kunci"]
            .astype(str)
            .str.lower()
        )

        text = str(text).lower()

        # Prioritas kata yang lebih spesifik/panjang
        kamus = kamus.sort_values(
            by="kata_kunci",
            key=lambda x: x.str.len(),
            ascending=False
        )

        for _, row in kamus.iterrows():

            if row["kata_kunci"] in text:
                return row["kategori"]

    except Exception:
        return None

    return None


def show():

    st.title("🔍 Prediksi Tingkat Kejahatan")

    st.write(
        "Masukkan judul berita untuk menentukan tingkat kejahatan berdasarkan kamus kejahatan."
    )

    judul = st.text_area(
        "Judul Berita",
        height=120,
        placeholder="Contoh: Polisi menangkap pelaku pembunuhan..."
    )


    if "riwayat_prediksi" not in st.session_state:
        st.session_state.riwayat_prediksi = []

    if st.button("Prediksi"):

        if not judul.strip():

            st.warning("Masukkan judul berita terlebih dahulu.")
            return


        hasil = prediksi_kamus(judul)


        st.subheader("Hasil Prediksi")


        if hasil:

            st.success(
                f"Tingkat Kejahatan: {hasil}"
            )

            st.session_state.riwayat_prediksi.append({
                "Judul": judul,
                "Kategori": hasil
            })


        else:

            st.warning(
                "Kata kejahatan tidak ditemukan pada kamus."
            )

            st.session_state.riwayat_prediksi.append({
                "Judul": judul,
                "Kategori": "Tidak ditemukan"
            })


        st.subheader("Riwayat Prediksi")

        riwayat = pd.DataFrame(st.session_state.riwayat_prediksi)
        st.dataframe(riwayat, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            csv = riwayat.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Hasil Prediksi",
                csv,
                file_name="riwayat_prediksi.csv",
                mime="text/csv"
            )

        with col2:
            if st.button("🔁 Repeat"):
                st.session_state.riwayat_prediksi = []
                st.rerun()
