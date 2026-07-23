import streamlit as st

def show():

    # ==========================
    # HEADER
    # ==========================

    st.title("🛡️ KLASIFIKASI TINGKAT KEJAHATAN")

    st.markdown("""
    ## PENERAPAN MACHINE LEARNING MENGGUNAKAN ALGORITMA NAÏVE BAYES
    ### UNTUK KLASIFIKASI TINGKAT KEJAHATAN
    #### (STUDI KASUS DI POLRES PASAMAN)
    """)

    st.divider()

    # ==========================
    # DESKRIPSI
    # ==========================

    st.subheader("📖 Deskripsi")

    st.write("""
    Aplikasi ini digunakan untuk melakukan klasifikasi tingkat kejahatan
    berdasarkan judul berita menggunakan algoritma Naïve Bayes.

    Sistem melakukan proses:

    - Upload Dataset
    - Preprocessing
    - Pembentukan TF-IDF
    - Klasifikasi Naïve Bayes
    - Prediksi Tingkat Kejahatan
    """)

    st.divider()

    # ==========================
    # ALUR SISTEM
    # ==========================

    st.subheader("⚙️ Alur Sistem")

    st.markdown("""
    ```
    Upload Dataset
            │
            ▼
      Preprocessing
            │
            ▼
          TF-IDF
            │
            ▼
      Training Naïve Bayes
            │
            ▼
      Evaluasi Model
            │
            ▼
         Prediksi
    ```
    """)

    st.divider()

    # ==========================
    # FITUR
    # ==========================

    st.subheader("✨ Fitur Sistem")

    col1, col2 = st.columns(2)

    with col1:

        st.success("📂 Upload Dataset")

        st.success("🧹 Preprocessing")

        st.success("📝 TF-IDF")

    with col2:

        st.success("🤖 Klasifikasi")

        st.success("🔍 Prediksi")

        st.success("📄 Download Laporan")

    st.divider()

    # ==========================
    # INFORMASI
    # ==========================

    st.subheader("📊 Informasi")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            label="Dataset",
            value="-"
        )

    with c2:
        st.metric(
            label="Model",
            value="Naïve Bayes"
        )

    with c3:
        st.metric(
            label="Kelas",
            value="2"
        )

    with c4:
        st.metric(
            label="Status",
            value="Siap"
        )

    st.divider()

    # ==========================
    # FOOTER
    # ==========================

    st.caption("© 2026 | Teknik Informatika | Polres Pasaman")
