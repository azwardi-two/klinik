from app.core.database import SessionLocal
from app.models.pemeriksaan import Pemeriksaan
from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail
from app.models.nilai_normal import NilaiNormal
from app.models.jenis_tabung import JenisTabung
from app.models.barang import Barang, PenerimaanBarang
from app.models.pemeriksaan_jenis_tabung import PemeriksaanJenisTabung


def _build_px_map(db):
    rows = db.query(Pemeriksaan).all()
    return {r.nama_pemeriksaan: r.id_pemeriksaan for r in rows}


def seed():
    db = SessionLocal()

    try:
        # -- PEMERIKSAAN --
        if db.query(Pemeriksaan).count() == 0:
            print("-- Seeding Pemeriksaan --")
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
            for d in pemeriksaan_data:
                p = Pemeriksaan(nama_pemeriksaan=d["nama"], biaya=d["biaya"], lama_waktu=d["waktu"], kategori=d["kat"], jenis_nilai=d["jenis"], satuan=d["satuan"])
                db.add(p)
                db.flush()
                print(f"  + Pemeriksaan: {p.nama_pemeriksaan} (id={p.id_pemeriksaan})")

        px_map = _build_px_map(db)

        # -- NILAI NORMAL --
        if db.query(NilaiNormal).count() == 0:
            print("\n-- Seeding Nilai Normal --")
            normal_data = [
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
                n = NilaiNormal(id_pemeriksaan=id_px, jenis_kelamin=nd[1], usia_hari_min=nd[2], usia_hari_max=nd[3], nilai_bawah=nd[4], nilai_atas=nd[5], operator=nd[6], nilai_operator=nd[7], nilai_text=nd[8])
                db.add(n)
                print(f"  + Nilai Normal: {nd[0]}")

        # -- PAKET PEMERIKSAAN --
        if db.query(PaketPemeriksaan).count() == 0:
            print("\n-- Seeding Paket Pemeriksaan --")
            paket_data = [
                {"nama": "Paket Darah Lengkap", "biaya": 70000, "ket": "Hemoglobin, Leukosit, Eritrosit, Trombosit, Hematokrit",
                 "items": ["Hemoglobin (Hb)", "Leukosit", "Eritrosit", "Trombosit", "Hematokrit"]},
                {"nama": "Paket Fungsi Hati", "biaya": 65000, "ket": "SGOT, SGPT",
                 "items": ["SGOT", "SGPT"]},
            ]
            for pd in paket_data:
                paket = PaketPemeriksaan(nama_paket=pd["nama"], biaya_paket=pd["biaya"], keterangan=pd["ket"])
                db.add(paket)
                db.flush()
                for item_nama in pd["items"]:
                    id_px = px_map.get(item_nama)
                    if id_px:
                        db.add(PaketPemeriksaanDetail(id_paket=paket.id_paket, id_pemeriksaan=id_px))
                print(f"  + Paket: {paket.nama_paket} (id={paket.id_paket})")

        # -- JENIS TABUNG --
        jt_map = {}
        if db.query(JenisTabung).count() == 0:
            print("\n--- Seeding Jenis Tabung ---")
            tabung_data = [
                {"nama": "EDTA", "warna": "Ungu", "volume": 3.0, "ket": "Antikoagulan untuk hematologi"},
                {"nama": "SST Gel", "warna": "Kuning", "volume": 5.0, "ket": "Serum separator untuk kimia darah"},
                {"nama": "Citrate 3.2%", "warna": "Biru Tua", "volume": 2.7, "ket": "Antikoagulan untuk pembekuan darah"},
                {"nama": "Heparin", "warna": "Hijau", "volume": 5.0, "ket": "Antikoagulan untuk elektrolit"},
                {"nama": "NaF / Oksalat", "warna": "Abu-abu", "volume": 3.0, "ket": "Untuk pemeriksaan gula darah"},
            ]
            for td in tabung_data:
                jt = JenisTabung(nama_jenis_tabung=td["nama"], warna=td["warna"], volume_ml=td["volume"], keterangan=td["ket"])
                db.add(jt)
                db.flush()
                jt_map[td["nama"]] = jt.id_jenis_tabung
                print(f"  + Jenis Tabung: {jt.nama_jenis_tabung} (id={jt.id_jenis_tabung})")
        else:
            for r in db.query(JenisTabung).all():
                jt_map[r.nama_jenis_tabung] = r.id_jenis_tabung

        # -- BARANG + STOK AWAL --
        if db.query(Barang).count() == 0:
            print("\n-- Seeding Barang & Stok Awal --")
            barang_data = [
                {"nama": "Tabung EDTA 3ml", "kat": "TABUNG", "satuan": "pcs", "harga": 2500, "min": 50, "jt": "EDTA"},
                {"nama": "Tabung SST 5ml", "kat": "TABUNG", "satuan": "pcs", "harga": 3500, "min": 30, "jt": "SST Gel"},
                {"nama": "Tabung Citrate 2.7ml", "kat": "TABUNG", "satuan": "pcs", "harga": 3000, "min": 20, "jt": "Citrate 3.2%"},
                {"nama": "Tabung Heparin 5ml", "kat": "TABUNG", "satuan": "pcs", "harga": 3500, "min": 20, "jt": "Heparin"},
                {"nama": "Tabung NaF 3ml", "kat": "TABUNG", "satuan": "pcs", "harga": 3000, "min": 20, "jt": "NaF / Oksalat"},
                {"nama": "Reagen Hematologi", "kat": "REAGEN", "satuan": "ml", "harga": 50000, "min": 100, "jt": None},
                {"nama": "Reagen Kimia Darah", "kat": "REAGEN", "satuan": "ml", "harga": 75000, "min": 100, "jt": None},
                {"nama": "Lancet", "kat": "BAHAN_PAKAI", "satuan": "pcs", "harga": 500, "min": 200, "jt": None},
                {"nama": "Kapas Alkohol", "kat": "BAHAN_PAKAI", "satuan": "pcs", "harga": 200, "min": 500, "jt": None},
                {"nama": "Sarung Tangan", "kat": "BAHAN_PAKAI", "satuan": "pasang", "harga": 1000, "min": 100, "jt": None},
            ]
            id_barang_list = []
            for bd in barang_data:
                id_jt = jt_map.get(bd["jt"]) if bd["jt"] else None
                b = Barang(id_jenis_tabung=id_jt, nama_barang=bd["nama"], kategori=bd["kat"], satuan=bd["satuan"], harga_satuan=bd["harga"], stok_minimum=bd["min"])
                db.add(b)
                db.flush()
                id_barang_list.append(b.id_barang)
                print(f"  + Barang: {b.nama_barang} (id={b.id_barang})")

            stok_awal = [
                (id_barang_list[0], 500), (id_barang_list[1], 200), (id_barang_list[2], 200),
                (id_barang_list[3], 200), (id_barang_list[4], 200), (id_barang_list[5], 500),
                (id_barang_list[6], 500), (id_barang_list[7], 1000), (id_barang_list[8], 2000),
                (id_barang_list[9], 500),
            ]
            for id_b, jml in stok_awal:
                db.add(PenerimaanBarang(id_barang=id_b, jumlah=jml))
                print(f"  + Stok awal: barang_id={id_b} = {jml}")

        # -- PEMERIKSAAN -> JENIS TABUNG --
        if db.query(PemeriksaanJenisTabung).count() == 0:
            print("\n-- Seeding Mapping Pemeriksaan -> Jenis Tabung --")
            mapping_data = [
                ("Hemoglobin (Hb)",     "EDTA"), ("Leukosit", "EDTA"), ("Eritrosit", "EDTA"),
                ("Trombosit", "EDTA"), ("Hematokrit", "EDTA"), ("Gula Darah Sewaktu", "NaF / Oksalat"),
                ("Kolesterol Total", "SST Gel"), ("Asam Urat", "SST Gel"), ("SGOT", "SST Gel"), ("SGPT", "SST Gel"),
            ]
            for nama_px, nama_jt in mapping_data:
                id_px = px_map.get(nama_px)
                id_jt = jt_map.get(nama_jt)
                if id_px and id_jt:
                    db.add(PemeriksaanJenisTabung(id_pemeriksaan=id_px, id_jenis_tabung=id_jt))
                    print(f"  + Mapping: {nama_px} -> {nama_jt}")

        db.commit()
        print("\n** Seeding selesai! **")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
