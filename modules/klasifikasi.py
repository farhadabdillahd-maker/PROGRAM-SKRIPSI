import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def show():

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

    # ===============================
    # Pastikan ada label
    # ===============================

    if "Pelabelan" not in df.columns:

        st.error("Kolom Pelabelan tidak ditemukan.")

        return

    X = st.session_state["tfidf_matrix"]

    y = df["Pelabelan"]

    st.success("Dataset siap digunakan.")

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

        20

    )

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
            average="weighted",
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            y_pred,
            average="weighted",
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            y_pred,
            average="weighted",
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

        # =======================================
        # CLASSIFICATION REPORT
        # =======================================

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0,
        )

        report_df = pd.DataFrame(report).transpose()

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
        st.subheader("Confusion Matrix")

        cm = confusion_matrix(y_test, y_pred)

        st.session_state["confusion_matrix"] = cm

        fig, ax = plt.subplots(figsize=(6, 5))

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=model.classes_
        )

        disp.plot(
            cmap="Blues",
            ax=ax,
            colorbar=False
        )

        ax.set_title("Confusion Matrix")
        ax.set_xlabel("Prediksi")
        ax.set_ylabel("Aktual")

        st.pyplot(fig)

        # =======================================
        # TAMPILKAN MATRIX DALAM TABEL
        # =======================================

        st.subheader("Tabel Confusion Matrix")

        cm_df = pd.DataFrame(
            cm,
            index=[f"Aktual {c}" for c in model.classes_],
            columns=[f"Prediksi {c}" for c in model.classes_]
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
        st.subheader("Hasil Prediksi Data Testing")

        hasil_prediksi = pd.DataFrame({

            "Data Asli": y_test.reset_index(drop=True),

            "Hasil Prediksi": pd.Series(y_pred),

            "Status": [
                "Benar" if a == b else "Salah"
                for a, b in zip(
                    y_test.reset_index(drop=True),
                    y_pred
                )
            ]

        })

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
