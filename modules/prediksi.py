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

            probabilitas = pd.DataFrame({

                "Kategori": [hasil],

                "Keterangan": [
                    "Ditentukan berdasarkan kamus kejahatan"
                ]

            })


        else:

            st.warning(
                "Kata kejahatan tidak ditemukan pada kamus."
            )

            probabilitas = pd.DataFrame({

                "Kategori": [
                    "Tidak ditemukan"
                ],

                "Keterangan": [
                    "Tambahkan kata tersebut ke kamus_kejahatan.csv"
                ]

            })


        st.subheader("Informasi Prediksi")

        st.dataframe(
            probabilitas,
            use_container_width=True
        )


        csv = probabilitas.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "📥 Download Hasil Prediksi",
            csv,
            file_name="hasil_prediksi_kamus.csv",
            mime="text/csv"
        )
