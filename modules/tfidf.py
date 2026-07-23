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
        # =====================================
    # TERM FREQUENCY (TF)
    # =====================================

    st.subheader("Term Frequency (TF)")

    tf_dict = {}

    # Hitung TF setiap term pada setiap dokumen
    for term in vocabulary:

        tf_dict[term] = []

        for tokens in tokenized_docs:

            counter = Counter(tokens)

            tf_dict[term].append(counter[term])

    # Membuat DataFrame TF

    tf_df = pd.DataFrame(tf_dict).T

    tf_df.columns = [

        f"d{i+1}"

        for i in range(total_document)

    ]

    tf_df.index.name = "Term"

    tf_df.reset_index(inplace=True)

    tf_df.insert(0, "No", range(1, len(tf_df)+1))

    st.dataframe(

        tf_df,

        use_container_width=True

    )

    # Simpan TF

    st.session_state["tf"] = tf_df

    st.divider()
        # =====================================
    # DOCUMENT FREQUENCY (DF)
    # =====================================

    df_dict = {}

    for term in vocabulary:

        jumlah_df = 0

        for tokens in tokenized_docs:

            if term in tokens:

                jumlah_df += 1

        df_dict[term] = jumlah_df

    # =====================================
    # INVERSE DOCUMENT FREQUENCY (IDF)
    # =====================================

    idf_dict = {}

    for term in vocabulary:

        df_value = df_dict[term]

        if df_value == 0:

            idf = 0

        else:

            idf = round(math.log10(total_document / df_value), 4)

        idf_dict[term] = idf

    # =====================================
    # TABEL DF DAN IDF
    # =====================================

    idf_df = pd.DataFrame({

        "No": range(1, len(vocabulary)+1),

        "Term": vocabulary,

        "DF": [df_dict[t] for t in vocabulary],

        "IDF": [idf_dict[t] for t in vocabulary]

    })

    st.subheader("Document Frequency (DF) dan Inverse Document Frequency (IDF)")

    st.dataframe(

        idf_df,

        use_container_width=True

    )

    # Simpan

    st.session_state["df"] = df_dict

    st.session_state["df"] = df_dict
    st.session_state["idf"] = idf_dict

    st.divider()

    # =====================================
    # PERHITUNGAN TF-IDF
    # =====================================

    st.subheader("Perhitungan TF-IDF")

    tfidf_rows = []

    for term in vocabulary:
        row = []
        for tf in tf_dict[term]:
            row.append(round(tf * idf_dict[term], 4))
        tfidf_rows.append(row)

    tfidf_df = pd.DataFrame(
        tfidf_rows,
        index=vocabulary,
        columns=[f"d{i+1}" for i in range(total_document)]
    )

    st.dataframe(tfidf_df, use_container_width=True)

    # Matriks untuk Naive Bayes
    tfidf_matrix = tfidf_df.T

    st.session_state["tfidf_df"] = tfidf_df
    st.session_state["tfidf_matrix"] = tfidf_matrix
    st.session_state["vocabulary"] = vocabulary

    st.success("Perhitungan TF-IDF selesai.")
    st.success("Data siap digunakan pada menu Klasifikasi.")
