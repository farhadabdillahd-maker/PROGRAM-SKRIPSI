import streamlit as st
import pandas as pd


def show():

    st.title("📂 Upload Dataset")

    st.write(
        "Upload dataset berformat CSV yang berisi data berita kejahatan."
    )

    st.divider()

    if "upload_key" not in st.session_state:
        st.session_state["upload_key"] = 0

    uploaded_file = st.file_uploader(
        "Pilih file CSV",
        type=["csv"],
        key=f'upload_{st.session_state["upload_key"]}'
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            # Simpan ke session_state
            st.session_state["dataset"] = df

            st.success("✅ Dataset berhasil diupload.")

            st.subheader("Preview Dataset")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.divider()

            st.subheader("Informasi Dataset")

            col1, col2 = st.columns(2)

            with col1:

                st.info(f"Jumlah Data : {len(df)}")

                st.info(f"Jumlah Kolom : {len(df.columns)}")

            with col2:

                st.info(f"Nama Kolom : {', '.join(df.columns)}")

                st.info(f"Missing Value : {df.isnull().sum().sum()}")

            st.divider()

            if "Label" in df.columns:

                st.subheader("Distribusi Label")

                st.dataframe(
                    df["Label"].value_counts().rename_axis("Label").reset_index(name="Jumlah"),
                    use_container_width=True
                )
            st.divider()

            if st.button("🔁 Repeat Upload"):
                st.session_state.pop("dataset", None)
                st.session_state["upload_key"] += 1
                st.rerun()


        except Exception as e:

            st.error(f"Gagal membaca file : {e}")

    else:

        st.warning("Silakan upload dataset terlebih dahulu.")
