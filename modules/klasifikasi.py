
# PDF support imports
from reportlab.platypus import SimpleDocTemplate
import streamlit as st
import pandas as pd
import joblib
import os
import re
from modules.pdf_report import generate_pdf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB



# ===============================
# CSS MODERN EXPANDER
# ===============================
def _modern_expander_css():
    st.markdown("""
    <style>
    div[data-testid="stExpander"]{
        border:2px solid #2F80ED!important;
        border-radius:16px!important;
        overflow:hidden;
        margin-bottom:12px;
        box-shadow:0 4px 12px rgba(0,0,0,.08);
    }
    div[data-testid="stExpander"] details summary{
        background:linear-gradient(90deg,#1E3C72,#2A5298);
        color:white!important;
        font-weight:700;
        font-size:17px;
        border-radius:14px;
    }
    div[data-testid="stExpander"] details summary:hover{
        background:linear-gradient(90deg,#2A5298,#3B82F6);
    }
    </style>
    """, unsafe_allow_html=True)


def show():

    _modern_expander_css()
    st.title("🤖 Klasifikasi Naïve Bayes")

    # ===============================
    # Cek TF-IDF
    # ===============================

    if "tfidf_matrix" not in st.session_state:

        st.warning("Silakan lakukan proses TF-IDF terlebih dahulu.")

        return

    if "preprocessed" not in st.session_state:

        st.warning("Dataset belum tersedia.")

        return

    
    df = st.session_state["preprocessed"]

    # =======================================
    # MEMBACA KAMUS KEJAHATAN DAN PELABELAN
    # =======================================
    # Label ditentukan berdasarkan KATA KUNCI pada judul,
    # bukan berdasarkan jenis_perkara sebagai dictionary key.
    # Jika beberapa tingkat ditemukan sekaligus, digunakan prioritas:
    # Sangat Berat > Berat > Ringan.
    if os.path.exists("kamus_klasifikasi_kejahatan.csv"):

        kamus = pd.read_csv("kamus_klasifikasi_kejahatan.csv")

        if (
            "kata_kunci" in kamus.columns
            and "klasifikasi" in kamus.columns
        ):

            LABEL_PRIORITAS = {
                "Ringan": 1,
                "Berat": 2,
                "Sangat Berat": 3
            }

            # Bersihkan kamus dan buang hanya baris yang benar-benar identik.
            kamus = kamus.drop_duplicates().copy()
            kamus["kata_kunci"] = (
                kamus["kata_kunci"]
                .astype(str)
                .str.strip()
                .str.lower()
            )
            kamus["klasifikasi"] = (
                kamus["klasifikasi"]
                .astype(str)
                .str.strip()
            )

            # Hanya gunakan 3 kelas penelitian.
            kamus = kamus[
                kamus["klasifikasi"].isin(LABEL_PRIORITAS.keys())
            ].copy()

            # Urutkan kata kunci terpanjang terlebih dahulu agar
            # frasa yang lebih spesifik diperiksa lebih dahulu.
            daftar_kata_kunci = (
                kamus[["kata_kunci", "klasifikasi"]]
                .dropna()
                .drop_duplicates()
                .sort_values(
                    "kata_kunci",
                    key=lambda s: s.str.len(),
                    ascending=False
                )
                .values
                .tolist()
            )

            def normalisasi_teks(teks):
                teks = str(teks).lower()
                teks = re.sub(r"[^a-z0-9\\s]", " ", teks)
                teks = re.sub(r"\\s+", " ", teks).strip()
                return teks

            def cari_label_judul(judul):
                teks = normalisasi_teks(judul)
                label_ditemukan = []

                for kata_kunci, klasifikasi in daftar_kata_kunci:
                    kata_kunci = normalisasi_teks(kata_kunci)

                    if not kata_kunci:
                        continue

                    # Pencocokan frasa/kata kunci.
                    pola = r"(?<![a-z0-9])" + re.escape(kata_kunci) + r"(?![a-z0-9])"

                    if re.search(pola, teks):
                        label_ditemukan.append(klasifikasi)

                if not label_ditemukan:
                    return None

                # Prioritas: Sangat Berat > Berat > Ringan.
                return max(
                    label_ditemukan,
                    key=lambda x: LABEL_PRIORITAS.get(x, 0)
                )

            if "Judul Media Nasional" not in df.columns:
                st.error("Kolom 'Judul Media Nasional' tidak ditemukan pada dataset.")
                return

            # Label utama berasal dari kata kunci pada judul.
            df["Pelabelan"] = df["Judul Media Nasional"].apply(cari_label_judul)

            # Fallback hanya untuk data yang tidak menemukan kata kunci:
            # gunakan klasifikasi yang paling sering muncul untuk jenis perkara
            # tersebut di kamus.
            if "Jenis Perkara" in df.columns and "jenis_perkara" in kamus.columns:
                kamus["jenis_perkara_norm"] = (
                    kamus["jenis_perkara"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                fallback_mapping = (
                    kamus.groupby("jenis_perkara_norm")["klasifikasi"]
                    .agg(lambda s: s.value_counts().index[0])
                    .to_dict()
                )

                mask_belum_berlabel = df["Pelabelan"].isna()

                df.loc[mask_belum_berlabel, "Pelabelan"] = (
                    df.loc[mask_belum_berlabel, "Jenis Perkara"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .map(fallback_mapping)
                )

            jumlah_belum_berlabel = df["Pelabelan"].isna().sum()

            if jumlah_belum_berlabel > 0:
                st.warning(
                    f"{jumlah_belum_berlabel} data belum dapat diberi label "
                    "dari kata kunci maupun fallback jenis perkara."
                )

            # Normalisasi label dan simpan.
            df["Pelabelan"] = df["Pelabelan"].astype("string").str.strip()

            st.session_state["preprocessed"] = df

        else:
            st.error(
                "Kamus harus memiliki kolom 'kata_kunci' dan 'klasifikasi'."
            )
            return
    else:
        st.error("File kamus_klasifikasi_kejahatan.csv tidak ditemukan.")
        return


    # ===============================
    # Pastikan ada label
    # ===============================

    if "Pelabelan" not in df.columns:

        st.error("Kolom Pelabelan tidak ditemukan.")

        return

    X = st.session_state["tfidf_matrix"]

    y = df["Pelabelan"]

    # Buang hanya baris yang benar-benar belum memiliki label.
    mask_valid = y.notna() & y.isin(["Ringan", "Berat", "Sangat Berat"])

    if not mask_valid.all():
        jumlah_dibuang = int((~mask_valid).sum())
        st.warning(
            f"{jumlah_dibuang} data tanpa label valid tidak digunakan dalam training."
        )
        df = df.loc[mask_valid].copy()
        X = X[mask_valid.to_numpy()]
        y = df["Pelabelan"]

    # Urutan kelas penelitian dibuat tetap.
    LABELS = ["Ringan", "Berat", "Sangat Berat"]

    st.success("Dataset siap digunakan.")

    # ===============================
    # VALIDASI LABEL DATASET
    # ===============================
    st.subheader("📋 Validasi Dataset")

    distribusi_label = (
        y.value_counts(dropna=False)
        .rename_axis("Label")
        .reset_index(name="Jumlah")
    )

    st.dataframe(distribusi_label, use_container_width=True)

    if y.isna().sum() > 0:
        st.warning(f"Terdapat {y.isna().sum()} data yang belum memiliki label.")
        data_nan = df[df["Pelabelan"].isna()]
        kolom = [c for c in ["Judul Media Nasional","Jenis Perkara","Pelabelan"] if c in data_nan.columns]
        st.dataframe(data_nan[kolom], use_container_width=True)

    st.write("Jumlah Data :", len(df))

    st.write("Jumlah Fitur :", X.shape[1])

    st.write("Jumlah Kelas :", len(y.unique()))

    st.divider()

    # =======================================
    # Train Test Split
    # =======================================

    test_size = st.slider(

        "Persentase Data Testing",

        10,

        50,

        30

    )

    
    # Pembagian default: 70% training dan 30% testing
    st.caption(
        f"Pembagian data: {100 - test_size}% training dan {test_size}% testing."
    )

    # Validasi tiga kelas penelitian.
    distribusi_tiga_kelas = y.value_counts().reindex(LABELS, fill_value=0)

    st.write("### Distribusi Label Sebelum Training")
    st.dataframe(
        distribusi_tiga_kelas.rename("Jumlah").reset_index().rename(
            columns={"index": "Label"}
        ),
        use_container_width=True
    )

    kelas_tanpa_data = distribusi_tiga_kelas[
        distribusi_tiga_kelas < 2
    ].index.tolist()

    if kelas_tanpa_data:
        st.error(
            "Kelas berikut memiliki kurang dari 2 data: "
            + ", ".join(kelas_tanpa_data)
            + ". Tambahkan data sebelum melakukan stratified split."
        )
        return

    if st.button("Training Naïve Bayes"):

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=test_size / 100,

            random_state=42,

            stratify=y

        )

        st.success("Train Test Split berhasil.")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Data Training",

                len(y_train)

            )

        with col2:

            st.metric(

                "Data Testing",

                len(y_test)

            )

        st.divider()

        # =======================================
        # Training
        # =======================================

        model = MultinomialNB()

        model.fit(

            X_train,

            y_train

        )


        st.success("Training Model Berhasil.")

        # =======================================
        # Simpan Session
        # =======================================

        st.session_state["model"] = model

        st.session_state["X_train"] = X_train

        st.session_state["X_test"] = X_test

        st.session_state["y_train"] = y_train

        st.session_state["y_test"] = y_test

        # =======================================
        # Simpan Model
        # =======================================

        # Membuat folder model otomatis jika belum tersedia
        os.makedirs("model", exist_ok=True)

        joblib.dump(

            model,

            "model/model_nb.pkl"

        )

        if "vectorizer" in st.session_state:
            joblib.dump(
                st.session_state["vectorizer"],
                "model/tfidf.pkl"
            )

        st.success("Model berhasil disimpan.")

        # ===============================
        # DEBUG PENYIMPANAN MODEL
        # ===============================
        st.subheader("Debug Model")
        st.write("model_nb.pkl :", os.path.exists("model/model_nb.pkl"))
        st.write("tfidf.pkl :", os.path.exists("model/tfidf.pkl"))

        if "vectorizer" in st.session_state:
            st.write("Jumlah fitur vectorizer :", len(st.session_state["vectorizer"].get_feature_names_out()))

        st.write("Jumlah fitur model :", model.n_features_in_)
        st.write("")
        st.subheader("📊 1️⃣ Prior Probability")

        prior_df = (
            y_train.value_counts(normalize=True)
            .sort_index()
            .reset_index()
        )
        prior_df.columns = ["Kelas", "Prior Probability"]
        prior_df["Prior Probability"] = prior_df["Prior Probability"].round(6)

        st.dataframe(prior_df, use_container_width=True)
        st.divider()

        st.divider()
        st.subheader("📊 2️⃣ Conditional Probability (Likelihood)")

        if "vectorizer" in st.session_state:
            feature_names = st.session_state["vectorizer"].get_feature_names_out()

            likelihood_df = pd.DataFrame(
                np.exp(model.feature_log_prob_).T,
                index=feature_names,
                columns=model.classes_
            ).reset_index()

            likelihood_df.rename(columns={"index": "Kata"}, inplace=True)

            st.write(f"Menampilkan seluruh {len(likelihood_df)} fitur beserta probabilitas kemunculannya pada setiap kelas.")

            st.dataframe(
                likelihood_df,
                use_container_width=True,
                height=600
            )

            csv_likelihood = likelihood_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Conditional Probability",
                data=csv_likelihood,
                file_name="conditional_probability_likelihood.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.session_state["likelihood"] = likelihood_df
        else:
            st.warning("Vectorizer tidak ditemukan sehingga Conditional Probability tidak dapat ditampilkan.")


              # =======================================
        # PREDIKSI DATA TESTING
        # =======================================

        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            classification_report,
        )

        y_pred = model.predict(X_test)

        st.session_state["y_pred"] = y_pred

        # =======================================
        # HITUNG METRIK
        # =======================================

        accuracy = accuracy_score(y_test, y_pred)

        precision = precision_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )

        # =======================================
        # SIMPAN KE SESSION STATE
        # =======================================

        st.session_state["accuracy"] = accuracy
        st.session_state["precision"] = precision
        st.session_state["recall"] = recall
        st.session_state["f1"] = f1

        # =======================================
        # TAMPILKAN HASIL EVALUASI
        # =======================================

        st.divider()
        with st.expander("📊 2️⃣ Hasil Evaluasi Model", expanded=True):
            st.subheader("📊 Hasil Evaluasi Model")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Accuracy",
                    value=f"{accuracy * 100:.2f}%"
                )

                st.metric(
                    label="Precision",
                    value=f"{precision * 100:.2f}%"
                )

            with col2:
                st.metric(
                    label="Recall",
                    value=f"{recall * 100:.2f}%"
                )


                st.metric(
                    label="F1-Score",
                    value=f"{f1 * 100:.2f}%"
                )

        with st.expander("📈 3️⃣ Distribusi Data", expanded=False):
            st.subheader("Distribusi Data")

            distribusi = y.value_counts().sort_index()
            tabel_distribusi = (
                distribusi.rename_axis("Kelas")
                .reset_index(name="Jumlah Data")
            )
            st.dataframe(tabel_distribusi, use_container_width=True)

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                fig_bar, ax_bar = plt.subplots(figsize=(4,3))
                ax_bar.bar(distribusi.index.astype(str), distribusi.values)
                ax_bar.set_title("Distribusi Data")
                ax_bar.set_xlabel("Kelas")
                ax_bar.set_ylabel("Jumlah")
                bar_chart_path = "bar_chart.png"
                fig_bar.savefig(bar_chart_path, dpi=300, bbox_inches="tight")
                st.pyplot(fig_bar)

            with col_chart2:
                fig_pie, ax_pie = plt.subplots(figsize=(4,3))
                ax_pie.pie(
                    distribusi.values,
                    labels=distribusi.index.astype(str),
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax_pie.set_title("Persentase Distribusi Data")
                ax_pie.axis("equal")
                pie_chart_path = "pie_chart.png"
                fig_pie.savefig(pie_chart_path, dpi=300, bbox_inches="tight")
                st.pyplot(fig_pie)


            # =======================================
            # CLASSIFICATION REPORT
            # =======================================

            report = classification_report(
                y_test,
                y_pred,
                labels=LABELS,
                target_names=LABELS,
                output_dict=True,
                zero_division=0,
            )

            # Tampilkan hanya metrik untuk 3 kelas penelitian.
            # Baris "macro avg" dan "weighted avg" sengaja dihapus.
            report_df = (
                pd.DataFrame(report).transpose()
                .loc[LABELS, ["precision", "recall", "f1-score", "support"]]
            )

            # Tambahkan accuracy sebagai baris terpisah tanpa macro/weighted avg.
            report_df.loc["accuracy"] = [
                accuracy,
                accuracy,
                accuracy,
                len(y_test),
            ]

        with st.expander("📋 4️⃣ Classification Report", expanded=False):
            st.subheader("Classification Report")

            st.dataframe(
                report_df,
                use_container_width=True,
            )

            st.session_state["classification_report"] = report_df
                  # =======================================
            # CONFUSION MATRIX
            # =======================================

            st.divider()
        with st.expander("🧩 5️⃣ Confusion Matrix", expanded=False):
            st.subheader("Confusion Matrix")

            cm = confusion_matrix(
                y_test,
                y_pred,
                labels=LABELS
            )

            st.session_state["confusion_matrix"] = cm

            fig, ax = plt.subplots(figsize=(2.4, 2.2))

            disp = ConfusionMatrixDisplay(
                confusion_matrix=cm,
                display_labels=LABELS
            )

            disp.plot(
                cmap="Blues",
                ax=ax,
                colorbar=False,
                values_format='d'
            )

            ax.set_title("Confusion Matrix", fontsize=10)
            ax.tick_params(axis="both", labelsize=8)
            ax.set_xlabel("Prediksi")
            ax.set_ylabel("Aktual", fontsize=8)
            ax.set_xlabel("Prediksi", fontsize=8)
            ax.set_title("Confusion Matrix", fontsize=9)
            ax.tick_params(axis="both", labelsize=7)
            plt.tight_layout()

            cm_image_path = "confusion_matrix.png"
            fig.savefig(cm_image_path, dpi=300, bbox_inches="tight")
            _, c, _ = st.columns([1,2,1])
            with c:
                st.pyplot(fig, use_container_width=False)

            # =======================================
            # TAMPILKAN MATRIX DALAM TABEL
            # =======================================

        with st.expander("📑 6️⃣ Tabel Confusion Matrix", expanded=False):
            st.subheader("Tabel Confusion Matrix")

            cm_df = pd.DataFrame(
                cm,
                index=[f"Aktual {c}" for c in LABELS],
                columns=[f"Prediksi {c}" for c in LABELS]
            )

            st.dataframe(
                cm_df,
                use_container_width=True
            )

            st.session_state["cm_df"] = cm_df

            # =======================================
            # RINGKASAN HASIL
            # =======================================

            st.divider()
        with st.expander("📌 7️⃣ Ringkasan Model", expanded=False):
            st.subheader("Ringkasan Model")

            st.success("Model Naïve Bayes berhasil dilatih.")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Jumlah Data Training**")
                st.info(len(y_train))

                st.write("**Jumlah Data Testing**")
                st.info(len(y_test))

            with col2:
                st.write("**Jumlah Fitur**")
                st.info(X.shape[1])

                st.write("**Jumlah Kelas**")
                st.info(len(model.classes_))

            st.divider()

        with st.expander("📝 8️⃣ Kesimpulan", expanded=False):
            st.subheader("Kesimpulan")

            st.write(
                f"""
Model Naïve Bayes telah berhasil dilatih menggunakan
**{len(y_train)} data training** dan diuji menggunakan
**{len(y_test)} data testing**.

Model menghasilkan nilai:

- Accuracy : **{accuracy*100:.2f}%**
- Precision : **{precision*100:.2f}%**
- Recall : **{recall*100:.2f}%**
- F1-Score : **{f1*100:.2f}%**

Semakin tinggi nilai Accuracy, Precision, Recall, dan F1-Score,
maka semakin baik performa model dalam mengklasifikasikan tingkat
kejahatan.
"""
            )

            st.balloons()
            # =======================================
            # PROBABILITAS PREDIKSI
            # =======================================

            st.divider()
        with st.expander("📈 9️⃣ Probabilitas Prediksi", expanded=False):
            st.subheader("Probabilitas Prediksi")

            probability = model.predict_proba(X_test)

            probability_df = pd.DataFrame(
                probability,
                columns=model.classes_
            )

            st.dataframe(
                probability_df,
                use_container_width=True
            )

            st.session_state["probability"] = probability_df

            # =======================================
            # HASIL PREDIKSI
            # =======================================

            st.divider()
        with st.expander("📰 🔟 Hasil Prediksi Testing", expanded=True):
            st.subheader("Hasil Prediksi Judul Berita Testing")

            # Mengambil judul berita asli berdasarkan index data testing
            judul_testing = df.loc[
                y_test.index,
                "Judul Media Nasional"
            ].reset_index(drop=True)

            hasil_prediksi = pd.DataFrame({

                "Judul Media Nasional": judul_testing,

                "Label Asli": y_test.reset_index(drop=True),

                "Hasil Prediksi": pd.Series(y_pred),

                "Status": [
                    "Benar" if a == b else "Salah"
                    for a, b in zip(
                        y_test.reset_index(drop=True),
                        y_pred
                    )
                ]

            })

            # Menampilkan hanya kolom hasil prediksi tanpa probabilitas
            hasil_prediksi = hasil_prediksi.reset_index(drop=True)

            st.dataframe(
                hasil_prediksi,
                use_container_width=True
            )

            st.session_state["hasil_prediksi"] = hasil_prediksi

            # =======================================
            # DOWNLOAD CSV
            # =======================================

            csv = hasil_prediksi.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(

                label="📥 Download Hasil Prediksi",

                data=csv,

                file_name="hasil_prediksi_naive_bayes.csv",

                mime="text/csv"

            )

            # =======================================
            # INFORMASI MODEL
            # =======================================

            st.divider()

        with st.expander("ℹ️ 1️⃣1️⃣ Informasi Model", expanded=False):
            st.subheader("Informasi Model")

            info_model = pd.DataFrame({

                "Parameter": [

                    "Algoritma",

                    "Jumlah Data Training",

                    "Jumlah Data Testing",

                    "Jumlah Fitur",

                    "Jumlah Kelas"

                ],

                "Nilai": [

                    "Multinomial Naïve Bayes",

                    len(y_train),

                    len(y_test),

                    X.shape[1],

                    len(model.classes_)

                ]

            })

            st.dataframe(
                info_model,
                use_container_width=True
            )

            # =======================================
            # PESAN AKHIR
            # =======================================

            st.success(
                "Seluruh proses klasifikasi berhasil dijalankan."
            )


            st.balloons()

        # end informasi model

        # =======================================
        # DOWNLOAD LAPORAN PDF
        # =======================================

        st.divider()
        st.subheader("📄 Laporan Hasil Klasifikasi")

        st.info(
            "Klik tombol di bawah untuk mengunduh laporan lengkap hasil "
            "klasifikasi dalam format PDF."
        )

        from datetime import datetime

        pdf_file = generate_pdf(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            report_df=report_df,
            cm_df=cm_df,
            hasil_prediksi=hasil_prediksi,
            bar_chart_path=bar_chart_path,
            pie_chart_path=pie_chart_path,
            info_model=info_model,
            waktu_download=datetime.now(),
        )

        with open(pdf_file, "rb") as pdf:
            pdf_bytes = pdf.read()

        st.download_button(
            label="📥 Download Laporan PDF",
            data=pdf_bytes,
            file_name=pdf_file,
            mime="application/pdf",
            use_container_width=True,
        )


# === PETUNJUK ===
# Tambahkan fungsi generate_pdf() dan st.download_button() sesuai contoh yang telah diberikan
# untuk menghasilkan laporan PDF.
