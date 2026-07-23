import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer


def show():

    st.title("📝 TF-IDF")

    # ==========================
    # Cek preprocessing
    # ==========================

    if "preprocessed" not in st.session_state:

        st.warning("Silakan lakukan preprocessing terlebih dahulu.")

        return

    df = st.session_state["preprocessed"]

    # ==========================
    # Tombol proses
    # ==========================

    if st.button("Proses TF-IDF"):

        vectorizer = TfidfVectorizer()

        X = vectorizer.fit_transform(df["Final Text"])

        feature_names = vectorizer.get_feature_names_out()

        tfidf_df = pd.DataFrame(
            X.toarray(),
            columns=feature_names
        )

        # ==========================
        # Simpan ke session_state
        # ==========================

        st.session_state["vectorizer"] = vectorizer
        st.session_state["tfidf_matrix"] = X
        st.session_state["feature_names"] = feature_names
        st.session_state["tfidf_dataframe"] = tfidf_df

        # ==========================
        # Informasi
        # ==========================

        st.success("TF-IDF berhasil dibuat.")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Jumlah Dokumen",
                X.shape[0]
            )

        with col2:

            st.metric(
                "Jumlah Vocabulary",
                X.shape[1]
            )

        st.divider()

        # ==========================
        # Vocabulary
        # ==========================

        st.subheader("Vocabulary")

        vocab_df = pd.DataFrame({

            "No": range(1, len(feature_names)+1),
            "Kata": feature_names

        })

        st.dataframe(
            vocab_df,
            use_container_width=True
        )

        st.divider()

        # ==========================
        # Matriks TF-IDF
        # ==========================

        st.subheader("Matriks TF-IDF")

        st.dataframe(
            tfidf_df,
            use_container_width=True
        )
