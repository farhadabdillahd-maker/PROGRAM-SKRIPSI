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
    info_model=None,
):
    """
    Menghasilkan laporan PDF hasil klasifikasi.
    Simpan logo pada:
        asset/logo_polri.png
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

    logo_polri = Image(os.path.join("asset","logo_polri.png"), width=2.8*CM, height=2.8*CM)
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

    elements.append(Spacer(1,1*CM))
    elements.append(Paragraph(
        "Demikian laporan hasil klasifikasi ini dibuat untuk dipergunakan sebagaimana mestinya.",
        normal))
    elements.append(Spacer(1,1*CM))
    elements.append(Paragraph(
        f"Pasaman, {datetime.now().strftime('%d %B %Y')}",
        normal))
    elements.append(Paragraph("Kepala Sat Reskrim",normal))
    elements.append(Spacer(1,2*CM))
    elements.append(Paragraph("(..........................................)",normal))

    doc.build(elements)

    output="Laporan_Hasil_Klasifikasi.pdf"
    with open(output,"wb") as f:
        f.write(buffer.getvalue())
    buffer.close()
    return output
