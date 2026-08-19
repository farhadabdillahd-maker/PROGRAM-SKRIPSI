
import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # Ambil hasil preprocessing
    # ================================
    documents = df["Final Text"].fillna("").astype(str).tolist()

    # ================================
    # Vectorizer (disimpan untuk prediksi)
    # ================================
    vectorizer = TfidfVectorizer(
        lowercase=False,
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )
    vectorizer.fit(documents)
    st.session_state["vectorizer"] = vectorizer

    # Tokenisasi
    tokenized_docs = [doc.split() for doc in documents]

    total_document = len(tokenized_docs)
    st.success(f"Jumlah Dokumen : {total_document}")
    st.divider()

    # Representasi Dokumen
    st.subheader("Tahapan Representasi Dokumen")
    representasi = {f"d{i+1}": len(tokens) for i, tokens in enumerate(tokenized_docs)}
    st.dataframe(pd.DataFrame([representasi]), use_container_width=True)

    st.divider()

    # Vocabulary
    vocabulary = sorted(set(token for doc in tokenized_docs for token in doc))
    st.success(f"Jumlah Term : {len(vocabulary)}")

    vocab_df = pd.DataFrame({
        "No": range(1, len(vocabulary)+1),
        "Term": vocabulary
    })
    st.subheader("Vocabulary")
    st.dataframe(vocab_df, use_container_width=True)

    # =====================================
    # WORD CLOUD / KATA PALING BANYAK MUNCUL
    # =====================================
    st.divider()
    st.subheader("☁️ Kata Paling Banyak Muncul")

    # Menghitung frekuensi setiap kata dari Final Text
    word_counter = Counter(
        word
        for tokens in tokenized_docs
        for word in tokens
        if word.strip()
    )

    if word_counter:
        jumlah_kata = st.slider(
            "Jumlah kata yang ditampilkan",
            min_value=5,
            max_value=min(30, len(word_counter)),
            value=min(15, len(word_counter))
        )

        top_words = word_counter.most_common(jumlah_kata)

        word_freq_df = pd.DataFrame(
            top_words,
            columns=["Kata", "Frekuensi"]
        )
        word_freq_df.insert(0, "No", range(1, len(word_freq_df) + 1))

        st.dataframe(
            word_freq_df,
            use_container_width=True,
            hide_index=True
        )

        # Grafik frekuensi kata
        fig_words, ax_words = plt.subplots(figsize=(10, 5))

        words = [item[0] for item in top_words]
        frequencies = [item[1] for item in top_words]

        # Dibalik agar kata dengan frekuensi tertinggi berada di atas
        ax_words.barh(words[::-1], frequencies[::-1])
        ax_words.set_title("Kata yang Paling Banyak Muncul")
        ax_words.set_xlabel("Frekuensi")
        ax_words.set_ylabel("Kata")

        for i, value in enumerate(frequencies[::-1]):
            ax_words.text(value, i, f" {value}", va="center")

        plt.tight_layout()
        st.pyplot(fig_words)

        # Word cloud visual jika library tersedia
        try:
            from wordcloud import WordCloud

            wordcloud = WordCloud(
                width=1200,
                height=500,
                background_color="white",
                colormap="Blues",
                max_words=jumlah_kata,
                collocations=False
            ).generate_from_frequencies(dict(top_words))

            fig_wc, ax_wc = plt.subplots(figsize=(12, 5))
            ax_wc.imshow(wordcloud, interpolation="bilinear")
            ax_wc.axis("off")
            ax_wc.set_title("Word Cloud Kata yang Paling Banyak Muncul")
            plt.tight_layout()
            st.pyplot(fig_wc)

        except ImportError:
            st.info(
                "Word Cloud tidak dapat ditampilkan karena library "
                "'wordcloud' belum terpasang. Grafik frekuensi kata tetap tersedia."
            )
    else:
        st.warning("Tidak terdapat kata untuk ditampilkan.")

    st.divider()

    # TF
    st.subheader("Term Frequency (TF)")
    tf_dict = {}
    for term in vocabulary:
        tf_dict[term] = []
        for tokens in tokenized_docs:
            tf_dict[term].append(Counter(tokens)[term])

    tf_df = pd.DataFrame(tf_dict).T
    tf_df.columns = [f"d{i+1}" for i in range(total_document)]
    tf_df.index.name = "Term"
    tf_df.reset_index(inplace=True)
    tf_df.insert(0, "No", range(1, len(tf_df)+1))
    st.dataframe(tf_df, use_container_width=True)

    st.divider()

    # DF
    df_dict = {}
    for term in vocabulary:
        df_dict[term] = sum(term in tokens for tokens in tokenized_docs)

    # Smoothed IDF
    idf_dict = {}
    N = total_document
    for term in vocabulary:
        df_value = df_dict[term]
        idf_dict[term] = round(math.log10((N + 1) / (df_value + 1)) + 1, 4)

    idf_df = pd.DataFrame({
        "No": range(1, len(vocabulary)+1),
        "Term": vocabulary,
        "DF": [df_dict[t] for t in vocabulary],
        "IDF": [idf_dict[t] for t in vocabulary]
    })

    st.subheader("Document Frequency (DF) dan Inverse Document Frequency (IDF)")
    st.dataframe(idf_df, use_container_width=True)

    st.session_state["df"] = df_dict
    st.session_state["idf"] = idf_dict

    st.divider()

    # TF-IDF
    st.subheader("Perhitungan TF-IDF")

    tfidf_rows = []
    for term in vocabulary:
        row = [round(tf * idf_dict[term], 4) for tf in tf_dict[term]]
        tfidf_rows.append(row)

    tfidf_df = pd.DataFrame(
        tfidf_rows,
        index=vocabulary,
        columns=[f"d{i+1}" for i in range(total_document)]
    )

    st.dataframe(tfidf_df, use_container_width=True)

    # =====================================
    # MATRIX TF-IDF UNTUK MACHINE LEARNING
    # Menggunakan TfidfVectorizer agar konsisten
    # dengan model Naive Bayes dan prediksi.
    # =====================================
    tfidf_matrix = vectorizer.fit_transform(documents)

    st.session_state["vectorizer"] = vectorizer
    st.session_state["tf"] = tf_df
    st.session_state["tfidf_df"] = tfidf_df
    st.session_state["tfidf_matrix"] = tfidf_matrix
    st.session_state["vocabulary"] = vocabulary

    st.success("Perhitungan TF-IDF selesai.")
    st.success("Data siap digunakan pada menu Klasifikasi.")
