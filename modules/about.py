import os
import streamlit as st

def show():
    st.title("👨‍💻 About Aplikasi")

    col1, col2 = st.columns([1, 2])

    with col1:
        foto = "asset/FOTO.png"
        if os.path.exists(foto):
            st.image(foto, width=220)
        else:
            st.info("Foto belum tersedia.\nSimpan sebagai asset/FOTO.png")

    with col2:
        st.markdown("## Penerapan Machine Learning Menggunakan Algoritma Naïve Bayes")
        st.markdown("### Untuk Klasifikasi Tingkat Kejahatan")
        st.markdown("**Studi Kasus: Polres Pasaman**")

        st.markdown("---")

        st.write("**Nama** : Farhad Abdillah Darnaz")
        st.write("**Jurusan** : Teknik Informatika")
        st.write("**Metode** : Naïve Bayes")
        st.write("**Ekstraksi Fitur** : TF-IDF")
        st.write("**Bahasa Pemrograman** : Python")
        st.write("**Framework** : Streamlit")

    st.markdown("---")

    st.subheader("Deskripsi Aplikasi")

    st.write(
        """
Aplikasi ini digunakan untuk mengklasifikasikan tingkat kejahatan
berdasarkan judul berita menggunakan algoritma Naïve Bayes.

Tahapan pengolahan data meliputi:
- Upload Dataset
- Case Folding
- Tokenizing
- Stopword Removal
- Stemming
- Perhitungan TF-IDF
- Klasifikasi Naïve Bayes
- Prediksi Tingkat Kejahatan

Aplikasi ini dikembangkan sebagai implementasi penelitian skripsi
Program Studi Teknik Informatika.
"""
    )

    st.markdown("---")

    st.subheader("Alur Sistem")

    st.markdown("""
1. Upload Dataset
2. Preprocessing
3. Perhitungan TF-IDF
4. Training Naïve Bayes
5. Evaluasi Model
6. Prediksi Tingkat Kejahatan
""")

    st.markdown("---")
    st.success("© 2026 Farhad Abdillah Darnaz")

