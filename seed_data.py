from app.core.database import SessionLocal
from app.models.pemeriksaan import Pemeriksaan
from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail
from app.models.nilai_normal import NilaiNormal


def seed():
    db = SessionLocal()

    try:
        existing = db.query(Pemeriksaan).count()
        if existing > 0:
            print(f"Data sudah ada ({existing} pemeriksaan), skip seeding")
            return

        # ── PEMERIKSAAN ──────────────────────────────────
        pemeriksaan_data = [
            {"nama": "Hemoglobin (Hb)", "biaya": 25000, "waktu": 30, "kat": "Hematologi", "jenis": "range", "satuan": "g/dL"},
            {"nama": "Leukosit", "biaya": 20000, "waktu": 30, "kat": "Hematologi", "jenis": "range", "satuan": "ribu/μL"},
            {"nama": "Eritrosit", "biaya": 20000, "waktu": 30, "kat": "Hematologi", "jenis": "range", "satuan": "juta/μL"},
            {"nama": "Trombosit", "biaya": 25000, "waktu": 30, "kat": "Hematologi", "jenis": "range", "satuan": "ribu/μL"},
            {"nama": "Hematokrit", "biaya": 20000, "waktu": 30, "kat": "Hematologi", "jenis": "range", "satuan": "%"},
            {"nama": "Gula Darah Sewaktu", "biaya": 30000, "waktu": 45, "kat": "Kimia Darah", "jenis": "operator", "satuan": "mg/dL"},
            {"nama": "Kolesterol Total", "biaya": 35000, "waktu": 45, "kat": "Kimia Darah", "jenis": "operator", "satuan": "mg/dL"},
            {"nama": "Asam Urat", "biaya": 35000, "waktu": 45, "kat": "Kimia Darah", "jenis": "range", "satuan": "mg/dL"},
            {"nama": "SGOT", "biaya": 40000, "waktu": 60, "kat": "Kimia Darah", "jenis": "range", "satuan": "U/L"},
            {"nama": "SGPT", "biaya": 40000, "waktu": 60, "kat": "Kimia Darah", "jenis": "range", "satuan": "U/L"},
        ]

        created = []
        for d in pemeriksaan_data:
            p = Pemeriksaan(nama_pemeriksaan=d["nama"], biaya=d["biaya"], lama_waktu=d["waktu"], kategori=d["kat"], jenis_nilai=d["jenis"], satuan=d["satuan"])
            db.add(p)
            db.flush()
            created.append(p)
            print(f"  + Pemeriksaan: {p.nama_pemeriksaan} (id={p.id_pemeriksaan})")

        # map nama → id
        px_map = {p.nama_pemeriksaan: p.id_pemeriksaan for p in created}

        # ── NILAI NORMAL ─────────────────────────────────
        normal_data = [
            # (nama_pemeriksaan, jk, usia_min, usia_max, bawah, atas, operator, op_val, text)
            ("Hemoglobin (Hb)",     "L", 0, 99999,  13.0, 17.0, None, None, None),
            ("Hemoglobin (Hb)",     "P", 0, 99999,  12.0, 15.0, None, None, None),
            ("Leukosit",            None, 0, 99999,  4.0, 10.0, None, None, None),
            ("Eritrosit",           "L", 0, 99999,  4.5, 5.5,  None, None, None),
            ("Eritrosit",           "P", 0, 99999,  4.0, 5.0,  None, None, None),
            ("Trombosit",           None, 0, 99999,  150.0, 450.0, None, None, None),
            ("Hematokrit",          "L", 0, 99999,  40.0, 50.0, None, None, None),
            ("Hematokrit",          "P", 0, 99999,  35.0, 45.0, None, None, None),
            ("Gula Darah Sewaktu",  None, 0, 99999,  None, None, "<", 200.0, None),
            ("Kolesterol Total",    None, 0, 99999,  None, None, "<", 200.0, None),
            ("Asam Urat",           "L", 0, 99999,  3.5, 7.0, None, None, None),
            ("Asam Urat",           "P", 0, 99999,  2.5, 6.0, None, None, None),
            ("SGOT",                None, 0, 99999,  10.0, 40.0, None, None, None),
            ("SGPT",                None, 0, 99999,  10.0, 40.0, None, None, None),
        ]

        for nd in normal_data:
            id_px = px_map.get(nd[0])
            if not id_px:
                continue
            n = NilaiNormal(
                id_pemeriksaan=id_px,
                jenis_kelamin=nd[1],
                usia_hari_min=nd[2],
                usia_hari_max=nd[3],
                nilai_bawah=nd[4],
                nilai_atas=nd[5],
                operator=nd[6],
                nilai_operator=nd[7],
                nilai_text=nd[8],
            )
            db.add(n)
            print(f"  + Nilai Normal: {nd[0]}")

        # ── PAKET PEMERIKSAAN ────────────────────────────
        paket_data = [
            {
                "nama": "Paket Darah Lengkap",
                "biaya": 70000,
                "ket": "Hemoglobin, Leukosit, Eritrosit, Trombosit, Hematokrit",
                "items": ["Hemoglobin (Hb)", "Leukosit", "Eritrosit", "Trombosit", "Hematokrit"],
            },
            {
                "nama": "Paket Fungsi Hati",
                "biaya": 65000,
                "ket": "SGOT, SGPT",
                "items": ["SGOT", "SGPT"],
            },
        ]

        for pd in paket_data:
            paket = PaketPemeriksaan(nama_paket=pd["nama"], biaya_paket=pd["biaya"], keterangan=pd["ket"])
            db.add(paket)
            db.flush()
            for item_nama in pd["items"]:
                id_px = px_map.get(item_nama)
                if id_px:
                    detail = PaketPemeriksaanDetail(id_paket=paket.id_paket, id_pemeriksaan=id_px)
                    db.add(detail)
            print(f"  + Paket: {paket.nama_paket} (id={paket.id_paket})")

        db.commit()
        print("\n✅ Seeding selesai!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
