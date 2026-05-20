from io import BytesIO
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
from fpdf import FPDF

from app.models.kunjungan import Kunjungan
from app.models.pasien import Pasien
from app.models.klinik import Klinik
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.models.pemeriksaan import Pemeriksaan
from app.models.nilai_normal import NilaiNormal


def _hitung_umur(tgl_lahir: date, tgl_kunjungan: date) -> str:
    diff = relativedelta(tgl_kunjungan, tgl_lahir)
    parts = []
    if diff.years:
        parts.append(f"{diff.years} tahun")
    if diff.months:
        parts.append(f"{diff.months} bulan")
    if diff.days:
        parts.append(f"{diff.days} hari")
    return " ".join(parts) if parts else "0 hari"


def _get_normal_match(db: Session, id_pemeriksaan: int, jenis_kelamin: Optional[str], umur_hari: Optional[int]):
    rows = db.query(NilaiNormal).filter(
        NilaiNormal.id_pemeriksaan == id_pemeriksaan
    ).all()
    for n in rows:
        if n.jenis_kelamin and jenis_kelamin and n.jenis_kelamin != jenis_kelamin:
            continue
        if umur_hari is not None and not (n.usia_hari_min <= umur_hari <= n.usia_hari_max):
            continue
        return n
    return rows[0] if rows else None


def _format_normal(n, jenis_nilai: str) -> str:
    if not n:
        return "-"
    if jenis_nilai == "range":
        bawah = f"{n.nilai_bawah:g}" if n.nilai_bawah is not None else "-"
        atas = f"{n.nilai_atas:g}" if n.nilai_atas is not None else "-"
        return f"{bawah} - {atas}"
    if jenis_nilai == "operator":
        op = n.operator or ""
        val = f"{n.nilai_operator:g}" if n.nilai_operator is not None else ""
        return f"{op} {val}".strip()
    if jenis_nilai == "text":
        return n.nilai_text or "-"
    return "-"


def _format_hasil(h: HasilPemeriksaan, jenis_nilai: str) -> str:
    if jenis_nilai == "text":
        return h.nilai_text or "-"
    if h.nilai_value is not None:
        return f"{h.nilai_value:g}"
    if h.nilai_bawah is not None and h.nilai_atas is not None:
        if h.nilai_bawah != h.nilai_atas:
            return f"{h.nilai_bawah:g} - {h.nilai_atas:g}"
        return f"{h.nilai_bawah:g}"
    if h.nilai_bawah is not None:
        return f"{h.nilai_bawah:g}"
    if h.nilai_atas is not None:
        return f"{h.nilai_atas:g}"
    return "-"


def _status_label(status: Optional[str]) -> str:
    if status == "H":
        return "T"
    if status == "L":
        return "R"
    if status == "N":
        return "N"
    return "-"


def _status_rgb(status: Optional[str]):
    if status == "H":
        return (217, 48, 37)
    if status == "L":
        return (26, 115, 232)
    if status == "N":
        return (24, 128, 56)
    return (102, 102, 102)


def generate_lab_pdf(db: Session, id_kunjungan: int) -> bytes:
    kunjungan = db.query(Kunjungan).filter(Kunjungan.id_kunjungan == id_kunjungan).first()
    if not kunjungan:
        raise ValueError("Kunjungan tidak ditemukan")

    pasien = db.query(Pasien).filter(Pasien.id == kunjungan.idpasien).first()
    if not pasien:
        raise ValueError("Pasien tidak ditemukan")

    klinik = db.query(Klinik).first()
    nama_klinik = klinik.nama if klinik else "NAMA KLINIK"
    alamat_klinik = klinik.alamat if klinik else ""
    telepon_klinik = klinik.telepon if klinik else ""

    umur_str = _hitung_umur(pasien.tgl_lahir, kunjungan.tgl_kunjungan)
    jenis_kelamin = pasien.jenis_kelamin
    umur_hari = kunjungan.umur_hari_pasien

    pp_rows = db.query(PemeriksaanPasien).filter(
        PemeriksaanPasien.id_kunjungan == id_kunjungan
    ).all()

    table_rows = []
    no = 0
    for pp in pp_rows:
        hasil_rows = db.query(HasilPemeriksaan).filter(
            HasilPemeriksaan.id_pemeriksaan_pasien == pp.id
        ).all()

        for h in hasil_rows:
            no += 1
            pemeriksaan = db.query(Pemeriksaan).filter(
                Pemeriksaan.id_pemeriksaan == h.id_pemeriksaan
            ).first()
            nama_periksa = pemeriksaan.nama_pemeriksaan if pemeriksaan else f"#{h.id_pemeriksaan}"
            jenis_nilai = pemeriksaan.jenis_nilai if pemeriksaan else "range"
            satuan = pemeriksaan.satuan or ""

            normal = _get_normal_match(db, h.id_pemeriksaan, jenis_kelamin, umur_hari)
            normal_str = _format_normal(normal, jenis_nilai)
            hasil_str = _format_hasil(h, jenis_nilai)
            label = _status_label(h.status_nilai)
            rgb = _status_rgb(h.status_nilai)

            table_rows.append({
                "no": str(no),
                "nama": nama_periksa,
                "hasil": hasil_str,
                "tanda": label,
                "tanda_rgb": rgb,
                "satuan": satuan,
                "normal": normal_str,
            })

    MARGIN = 10
    PAGE_W = 210
    WIDTH = PAGE_W - 2 * MARGIN
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # --- Header ---
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(WIDTH, 10, nama_klinik, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(85, 85, 85)
    pdf.cell(WIDTH, 6, alamat_klinik, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(WIDTH, 6, f"Telp: {telepon_klinik}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_draw_color(26, 115, 232)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(MARGIN, y, PAGE_W - MARGIN, y)
    pdf.ln(6)

    # --- Title ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(WIDTH, 8, "HASIL PEMERIKSAAN LABORATORIUM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # --- Patient Info (simple column layout to avoid overlap) ---
    pdf.set_text_color(0, 0, 0)
    label_w = 42
    sep_w = 5
    val_w = WIDTH - label_w - sep_w
    info = [
        ("No. Rekam Medis", pasien.no_rm or "-"),
        ("Nama Pasien", pasien.nama),
        ("Jenis Kelamin", "Laki-laki" if pasien.jenis_kelamin == "L" else "Perempuan" if pasien.jenis_kelamin == "P" else pasien.jenis_kelamin or "-"),
        ("Alamat", pasien.alamat or "-"),
        ("Umur", umur_str),
        ("Tanggal Kunjungan", kunjungan.tgl_kunjungan.strftime("%d %b %Y")),
    ]
    for label, value in info:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(label_w, 7, label, align="L")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(sep_w, 7, ":")
        pdf.cell(val_w, 7, value, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # --- Results Table ---
    col_widths = [8, 42, 22, 60, 26, 32]
    headers = ["No.", "Nama Pemeriksaan", "Hasil", "Nilai Normal", "Tanda", "Satuan"]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(26, 115, 232)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    if not table_rows:
        pdf.set_text_color(153, 153, 153)
        pdf.cell(sum(col_widths), 10, "Belum ada hasil pemeriksaan", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    else:
        for row in table_rows:
            pdf.set_text_color(0, 0, 0)
            pdf.cell(col_widths[0], 7, row["no"], border=1, align="C")
            pdf.cell(col_widths[1], 7, row["nama"], border=1, align="L")
            pdf.cell(col_widths[2], 7, row["hasil"], border=1, align="C")
            pdf.cell(col_widths[3], 7, row["normal"], border=1, align="L")
            r, g, b = row["tanda_rgb"]
            pdf.set_text_color(r, g, b)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(col_widths[4], 7, row["tanda"], border=1, align="C")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(col_widths[5], 7, row["satuan"], border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    # --- Legend ---
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(102, 102, 102)
    legend_y = pdf.get_y()
    pdf.set_text_color(217, 48, 37)
    pdf.cell(30, 5, "T = Tinggi", align="L")
    pdf.set_text_color(26, 115, 232)
    pdf.cell(30, 5, "R = Rendah", align="L")
    pdf.set_text_color(24, 128, 56)
    pdf.cell(30, 5, "N = Normal", align="L")
    pdf.ln(10)

    # --- Signature ---
    pdf.set_text_color(51, 51, 51)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(WIDTH, 6, "Mengetahui,", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(14)
    pdf.cell(WIDTH, 6, "Dokter", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    sig_x = PAGE_W - MARGIN - 50
    pdf.line(sig_x, pdf.get_y(), PAGE_W - MARGIN, pdf.get_y())
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(153, 153, 153)
    pdf.cell(WIDTH, 5, "( ___________________ )", align="R")

    return bytes(pdf.output())
