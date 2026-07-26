from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm as CM
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib.styles import ParagraphStyle
import os

def generate_pdf(
    accuracy,
    precision,
    recall,
    f1,
    report_df,
    cm_df,
    hasil_prediksi,
    bar_chart_path=None,
    pie_chart_path=None,
    info_model=None,
):
    """
    Menghasilkan laporan PDF hasil klasifikasi.
    Simpan logo pada:
        asset/logo_polri.jpg
        asset/logo_polda.png
    Jika ingin menambahkan logo dan confusion matrix sebagai gambar,
    tinggal dikembangkan pada fungsi ini.
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(21*CM,29.7*CM),
        rightMargin=1.5*CM,
        leftMargin=1.5*CM,
        topMargin=1.5*CM,
        bottomMargin=1.5*CM,
    )

    styles = getSampleStyleSheet()
    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    normal = styles["BodyText"]

    elements = []

    logo_polri = Image(os.path.join("asset","logo_polri.jpg"), width=2.8*CM, height=2.8*CM)
    logo_polda = Image(os.path.join("asset","logo_polda.png"), width=2.8*CM, height=2.8*CM)

    style_kop = ParagraphStyle(
        "kop",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
    )

    style_alamat = ParagraphStyle(
        "alamat",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
    )

    judul = Paragraph(
        "<b>KEPOLISIAN NEGARA REPUBLIK INDONESIA</b><br/><b>DAERAH SUMATERA BARAT</b><br/><b>RESOR PASAMAN</b>",
        style_kop
    )

    alamat = Paragraph(
        "Jln. Jend. Sudirman No. 1 Lubuk Sikaping 26311",
        style_alamat
    )

    kop = Table(
        [[logo_polri, [judul, alamat], logo_polda]],
        colWidths=[3.2*CM, 12*CM, 3.2*CM]
    )

    kop.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))

    elements.append(kop)

    garis = Table([[""]], colWidths=[18*CM], rowHeights=[0.05*CM])
    garis.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.black)]))
    elements.append(Spacer(1,0.12*CM))
    elements.append(garis)
    elements.append(Spacer(1,0.08*CM))
    elements.append(garis)
    elements.append(Spacer(1,0.4*CM))

    elements.append(Paragraph(
        "<b>LAPORAN HASIL KLASIFIKASI</b>",
        title))
    elements.append(Spacer(1,0.4*CM))

    nomor = f"B/001/RESKRIM/{datetime.now():%m/%Y}"

    info = [
        ["Parameter","Keterangan"],
        ["Nomor Surat",nomor],
        ["Tanggal",datetime.now().strftime("%d %B %Y")],
        ["Algoritma","Multinomial Naïve Bayes"],
        ["Accuracy",f"{accuracy*100:.2f}%"],
        ["Precision",f"{precision*100:.2f}%"],
        ["Recall",f"{recall*100:.2f}%"],
        ["F1-Score",f"{f1*100:.2f}%"],
    ]

    t=Table(info,colWidths=[6*CM,11*CM])
    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#d9e8ff")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,0),8),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    elements.append(t)

    elements.append(Paragraph("<b>Interpretasi Hasil Evaluasi Model</b>", styles["Heading3"]))
    elements.append(Paragraph(
        f"Berdasarkan hasil pengujian menggunakan algoritma <b>Multinomial Naïve Bayes</b>, "
        f"diperoleh nilai Accuracy sebesar <b>{accuracy*100:.2f}%</b>, Precision sebesar "
        f"<b>{precision*100:.2f}%</b>, Recall sebesar <b>{recall*100:.2f}%</b>, dan "
        f"F1-Score sebesar <b>{f1*100:.2f}%</b>. Nilai tersebut menunjukkan tingkat "
        f"kemampuan model dalam mengklasifikasikan data kejahatan berdasarkan dataset yang digunakan.",
        normal))
    elements.append(Spacer(1,0.5*CM))

    elements.append(Paragraph("<b>Classification Report</b>",styles["Heading3"]))
    rpt=[report_df.reset_index().columns.tolist()] + report_df.reset_index().round(4).astype(str).values.tolist()
    tr=Table(rpt)
    tr.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.3,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),
    ]))
    elements.append(tr)
    elements.append(Spacer(1,0.2*CM))
    elements.append(Paragraph(
        "Classification Report menyajikan nilai precision, recall, F1-score, dan support "
        "untuk setiap kelas. Semakin tinggi nilai precision, recall, dan F1-score, maka "
        "semakin baik performa model dalam mengklasifikasikan masing-masing kategori.",
        normal))
    elements.append(Spacer(1,0.5*CM))

    elements.append(Paragraph("<b>Confusion Matrix</b>",styles["Heading3"]))
    cm_table=[[""]+list(cm_df.columns)]
    for idx,row in zip(cm_df.index,cm_df.values.tolist()):
        cm_table.append([idx]+row)
    tc=Table(cm_table)
    tc.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.3,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ]))
    elements.append(tc)
    elements.append(Spacer(1,0.2*CM))
    elements.append(Paragraph(
        "Confusion Matrix digunakan untuk melihat jumlah prediksi yang benar dan salah. "
        "Nilai pada diagonal utama menunjukkan prediksi yang benar, sedangkan nilai di luar "
        "diagonal menunjukkan kesalahan klasifikasi yang masih dilakukan model.",
        normal))
    elements.append(Spacer(1,0.5*CM))


    if bar_chart_path and os.path.exists(bar_chart_path):
        elements.append(Paragraph("<b>Distribusi Dataset (Diagram Batang)</b>", styles["Heading3"]))
        elements.append(Image(bar_chart_path, width=16*CM, height=9*CM))
        elements.append(Paragraph(
            "Diagram batang menunjukkan jumlah data pada setiap kategori kelas. Grafik ini digunakan untuk melihat keseimbangan distribusi dataset yang digunakan dalam proses pelatihan model.",
            normal))
        elements.append(Spacer(1,0.5*CM))

    if pie_chart_path and os.path.exists(pie_chart_path):
        elements.append(Paragraph("<b>Distribusi Dataset (Diagram Lingkaran)</b>", styles["Heading3"]))
        elements.append(Image(pie_chart_path, width=12*CM, height=12*CM))
        elements.append(Paragraph(
            "Diagram lingkaran memperlihatkan persentase masing-masing kelas terhadap keseluruhan dataset sehingga memudahkan analisis proporsi data pada setiap kategori.",
            normal))
        elements.append(Spacer(1,0.5*CM))

    elements.append(Paragraph("<b>Hasil Prediksi Testing</b>",styles["Heading3"]))
    hp=[hasil_prediksi.columns.tolist()]
    hp += hasil_prediksi.head(20).astype(str).values.tolist()
    th=Table(hp)
    th.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.25,colors.black),
        ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),7),
    ]))
    elements.append(th)
    elements.append(Spacer(1,0.2*CM))
    elements.append(Paragraph(
        "Tabel Hasil Prediksi Testing menampilkan sebagian data uji beserta hasil prediksi "
        "yang diberikan oleh model. Bagian ini digunakan untuk melihat contoh hasil klasifikasi "
        "yang dihasilkan sistem terhadap data pengujian.",
        normal))

    elements.append(Spacer(1,1*CM))
    elements.append(Paragraph(
        "Demikian laporan hasil klasifikasi ini dibuat untuk dipergunakan sebagaimana mestinya.",
        normal))
    elements.append(Spacer(1,0.5*CM))
    elements.append(Paragraph("Demikian laporan hasil klasifikasi ini dibuat untuk dipergunakan sebagaimana mestinya.", normal))

    doc.build(elements)

    output="Laporan_Hasil_Klasifikasi.pdf"
    with open(output,"wb") as f:
        f.write(buffer.getvalue())
    buffer.close()
    return output
