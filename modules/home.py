import streamlit as st


def show():
    # =========================================================
    # ELEGANT HOME DASHBOARD
    # Tetap menggunakan fungsi show() agar mudah menggantikan
    # file home.py lama tanpa mengubah pemanggilan dari app.py.
    # =========================================================

    st.markdown("""
    <style>
    /* =========================
       GLOBAL
       ========================= */
    .home-wrap {
        width: 100%;
        max-width: 1220px;
        margin: 0 auto;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 42px 46px 38px 46px;
        border-radius: 30px;
        margin: 6px 0 26px 0;
        background:
            radial-gradient(circle at 88% 15%, rgba(66, 153, 225, .28), transparent 28%),
            radial-gradient(circle at 8% 90%, rgba(0, 191, 255, .16), transparent 30%),
            linear-gradient(135deg, #071a3a 0%, #0c2f63 48%, #123f7a 100%);
        box-shadow: 0 20px 55px rgba(8, 31, 72, .22);
        color: white;
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 250px;
        height: 250px;
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 50%;
        right: -80px;
        top: -90px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 50%;
        right: 10px;
        top: -45px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.14);
        backdrop-filter: blur(8px);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: .4px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: clamp(28px, 4vw, 46px);
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -1.5px;
        margin: 0;
        max-width: 780px;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.65;
        color: rgba(255,255,255,.82);
        margin: 18px 0 0 0;
        max-width: 760px;
    }

    .hero-tag {
        display: inline-block;
        margin-top: 22px;
        padding: 9px 15px;
        border-radius: 12px;
        background: rgba(255,255,255,.08);
        color: #eaf5ff;
        font-size: 13px;
        font-weight: 650;
        border: 1px solid rgba(255,255,255,.10);
    }

    /* =========================
       SECTION
       ========================= */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 30px 0 8px 0;
        color: #132b4f;
        font-size: 25px;
        font-weight: 800;
    }

    .section-subtitle {
        color: #66758a;
        font-size: 14px;
        margin: 0 0 18px 0;
    }

    /* =========================
       STAT CARDS
       ========================= */
    .stat-card {
        min-height: 135px;
        padding: 20px;
        border-radius: 22px;
        background: rgba(255,255,255,.88);
        border: 1px solid rgba(24, 62, 111, .09);
        box-shadow: 0 10px 30px rgba(20, 49, 88, .08);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 38px rgba(20, 49, 88, .13);
    }

    .stat-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .stat-label {
        color: #718096;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .stat-value {
        color: #102d55;
        font-size: 23px;
        font-weight: 850;
        margin-top: 4px;
    }

    .stat-note {
        color: #8491a3;
        font-size: 11px;
        margin-top: 5px;
    }

    /* =========================
       DESCRIPTION CARD
       ========================= */
    .info-card {
        padding: 26px 28px;
        border-radius: 24px;
        background: linear-gradient(145deg, #ffffff 0%, #f6faff 100%);
        border: 1px solid rgba(30, 76, 132, .08);
        box-shadow: 0 12px 35px rgba(22, 55, 96, .07);
    }

    .info-card h3 {
        color: #15345e;
        margin: 0 0 10px 0;
        font-size: 21px;
    }

    .info-card p {
        color: #526176;
        line-height: 1.7;
        font-size: 14px;
        margin-bottom: 0;
    }

    .mini-pill {
        display: inline-block;
        margin: 7px 6px 0 0;
        padding: 7px 11px;
        border-radius: 10px;
        background: #edf5ff;
        color: #174f91;
        font-size: 11px;
        font-weight: 750;
    }

    /* =========================
       PROCESS FLOW
       ========================= */
    .flow-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 9px;
        align-items: stretch;
        margin-top: 16px;
    }

    .flow-item {
        position: relative;
        text-align: center;
        padding: 18px 8px 16px 8px;
        border-radius: 18px;
        background: #fff;
        border: 1px solid #e4ebf4;
        box-shadow: 0 8px 24px rgba(20, 50, 90, .06);
    }

    .flow-number {
        width: 29px;
        height: 29px;
        line-height: 29px;
        margin: 0 auto 9px auto;
        border-radius: 50%;
        background: #0d4f94;
        color: white;
        font-size: 12px;
        font-weight: 800;
    }

    .flow-icon {
        font-size: 24px;
        margin-bottom: 6px;
    }

    .flow-name {
        color: #17385f;
        font-size: 12px;
        font-weight: 800;
        line-height: 1.35;
    }

    /* =========================
       FEATURE CARDS
       ========================= */
    .feature-card {
        height: 100%;
        min-height: 145px;
        padding: 22px;
        border-radius: 21px;
        background: #fff;
        border: 1px solid #e6edf5;
        box-shadow: 0 9px 27px rgba(20, 50, 90, .06);
        transition: all .2s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(33, 105, 178, .20);
        box-shadow: 0 15px 35px rgba(20, 50, 90, .11);
    }

    .feature-icon {
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: #edf5ff;
        font-size: 22px;
        margin-bottom: 13px;
    }

    .feature-title {
        color: #18385f;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .feature-text {
        color: #7a8799;
        font-size: 11px;
        line-height: 1.55;
    }

    /* =========================
       FOOTER
       ========================= */
    .home-footer {
        margin-top: 34px;
        padding: 20px 24px;
        border-radius: 20px;
        background: linear-gradient(135deg, #0b2852, #123f79);
        color: rgba(255,255,255,.78);
        text-align: center;
        font-size: 12px;
        box-shadow: 0 12px 30px rgba(8, 35, 76, .15);
    }

    .home-footer strong {
        color: white;
    }

    /* Streamlit cleanup */
    div[data-testid="stMarkdownContainer"] p {
        margin-bottom: .4rem;
    }

    @media (max-width: 900px) {
        .flow-grid {
            grid-template-columns: repeat(3, 1fr);
        }

        .hero {
            padding: 32px 28px;
        }
    }

    @media (max-width: 600px) {
        .flow-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .hero-title {
            font-size: 29px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # HERO
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="hero">
            <div class="hero-badge">🛡️ SISTEM KLASIFIKASI KEJAHATAN</div>
            <h1 class="hero-title">Klasifikasi Tingkat Kejahatan</h1>
            <p class="hero-subtitle">
                Penerapan Machine Learning menggunakan algoritma
                <strong>Naïve Bayes</strong> untuk membantu klasifikasi
                tingkat kejahatan berdasarkan judul berita.
            </p>
            <div class="hero-tag">📍 Studi Kasus: Polres Pasaman</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # QUICK OVERVIEW
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="section-title">📊 Ringkasan Sistem</div>
        <div class="section-subtitle">
            Gambaran singkat komponen utama yang digunakan dalam aplikasi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    stats = [
        ("🧠", "Model", "Naïve Bayes", "Multinomial"),
        ("📝", "Input", "Judul Berita", "Data teks"),
        ("🎯", "Klasifikasi", "Tingkat Kejahatan", "Berbasis kelas"),
        ("⚡", "Status", "Siap Digunakan", "Pipeline tersedia"),
    ]

    for col, (icon, label, value, note) in zip((c1, c2, c3, c4), stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-value">{value}</div>
                <div class="stat-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # DESKRIPSI
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="section-title">📖 Tentang Aplikasi</div>
        <div class="section-subtitle">
            Sistem dirancang dengan alur pengolahan teks hingga menghasilkan prediksi.
        </div>
        <div class="info-card">
            <h3>🔎 Klasifikasi berbasis teks</h3>
            <p>
                Aplikasi ini digunakan untuk melakukan klasifikasi tingkat kejahatan
                berdasarkan judul berita menggunakan algoritma Naïve Bayes.
                Data diproses melalui beberapa tahapan pengolahan teks sebelum
                digunakan pada proses klasifikasi dan prediksi.
            </p>
            <div style="margin-top:12px;">
                <span class="mini-pill">Case Folding</span>
                <span class="mini-pill">Tokenizing</span>
                <span class="mini-pill">Stopword Removal</span>
                <span class="mini-pill">Stemming</span>
                <span class="mini-pill">TF-IDF</span>
                <span class="mini-pill">Naïve Bayes</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # ALUR SISTEM
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="section-title">⚙️ Alur Sistem</div>
        <div class="section-subtitle">
            Tahapan utama dari dataset hingga menghasilkan prediksi.
        </div>

        <div class="flow-grid">
            <div class="flow-item">
                <div class="flow-number">01</div>
                <div class="flow-icon">📂</div>
                <div class="flow-name">Upload Dataset</div>
            </div>
            <div class="flow-item">
                <div class="flow-number">02</div>
                <div class="flow-icon">🧹</div>
                <div class="flow-name">Preprocessing</div>
            </div>
            <div class="flow-item">
                <div class="flow-number">03</div>
                <div class="flow-icon">📝</div>
                <div class="flow-name">TF-IDF</div>
            </div>
            <div class="flow-item">
                <div class="flow-number">04</div>
                <div class="flow-icon">🤖</div>
                <div class="flow-name">Training Naïve Bayes</div>
            </div>
            <div class="flow-item">
                <div class="flow-number">05</div>
                <div class="flow-icon">📈</div>
                <div class="flow-name">Evaluasi Model</div>
            </div>
            <div class="flow-item">
                <div class="flow-number">06</div>
                <div class="flow-icon">🔍</div>
                <div class="flow-name">Prediksi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # FITUR
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="section-title">✨ Fitur Utama</div>
        <div class="section-subtitle">
            Menu yang tersedia untuk mendukung proses penelitian.
        </div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3, gap="medium")

    features = [
        (f1, "📂", "Upload Dataset",
         "Memasukkan dataset berita sebagai sumber data klasifikasi."),
        (f1, "🧹", "Preprocessing",
         "Membersihkan dan menormalisasi teks sebelum proses pembelajaran."),
        (f1, "📝", "TF-IDF",
         "Mengubah teks menjadi representasi numerik berdasarkan bobot kata."),
        (f2, "🤖", "Klasifikasi",
         "Melakukan proses pembelajaran dan klasifikasi menggunakan Naïve Bayes."),
        (f2, "🔍", "Prediksi",
         "Menghasilkan prediksi tingkat kejahatan dari judul berita baru."),
        (f2, "📄", "Laporan",
         "Mendukung penyajian hasil prediksi dalam bentuk laporan."),
        (f3, "📊", "Evaluasi",
         "Menampilkan metrik untuk melihat performa model klasifikasi."),
        (f3, "🎯", "Confusion Matrix",
         "Membantu melihat hasil klasifikasi berdasarkan kelas aktual dan prediksi."),
        (f3, "⚡", "Interface Sederhana",
         "Tampilan terstruktur agar setiap tahapan mudah digunakan."),
    ]

    for col, icon, title, text in features:
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # FOOTER
    # =========================================================
    st.markdown("""
    <div class="home-wrap">
        <div class="home-footer">
            <strong>🛡️ KLASIFIKASI TINGKAT KEJAHATAN</strong><br>
            Penerapan Machine Learning menggunakan Algoritma Naïve Bayes
            <br>
            <span>Teknik Informatika • Studi Kasus Polres Pasaman • 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
