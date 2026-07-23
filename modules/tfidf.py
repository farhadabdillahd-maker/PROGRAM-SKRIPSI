import streamlit as st
import pandas as pd
import math
from collections import Counter


# =====================================
# HALAMAN TF-IDF
# =====================================

def show():

    st.title("📝 Perhitungan TF-IDF")

    if "preprocessed" not in st.session_state:

        st.warning("Silakan lakukan preprocessing terlebih dahulu.")

        return

    df = st.session_state["preprocessed"]

    # ================================
    # Ambil hasil stemming
    # ================================

    documents = df["Final Text"].tolist()

    # ================================
    # Pecah menjadi token
    # ================================

    tokenized_docs = []

    for doc in documents:

        tokenized_docs.append(doc.split())

    # ================================
    # Jumlah Dokumen
    # ================================

    total_document = len(tokenized_docs)

    st.success(f"Jumlah Dokumen : {total_document}")

    st.divider()

    # ================================
    # Representasi Dokumen
    # ================================

    st.subheader("Tahapan Representasi Dokumen")

    representasi = {}

    for i, tokens in enumerate(tokenized_docs):

        representasi[f"d{i+1}"] = len(tokens)

    representasi_df = pd.DataFrame(

        [representasi]

    )

    st.dataframe(

        representasi_df,

        use_container_width=True

    )

    st.divider()

    # ================================
    # Seluruh Term
    # ================================

    vocabulary = set()

    for tokens in tokenized_docs:

        vocabulary.update(tokens)

    vocabulary = sorted(list(vocabulary))

    st.success(

        f"Jumlah Term : {len(vocabulary)}"

    )

    st.divider()
