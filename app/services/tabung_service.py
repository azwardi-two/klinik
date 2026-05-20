import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.tabung import Tabung, TabungPemeriksaan
from app.models.pemeriksaan_lab import PemeriksaanLab
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.jenis_tabung import JenisTabung
from app.models.kunjungan import Kunjungan
from app.models.pasien import Pasien
from app.repositories.tabung import TabungRepository, TabungPemeriksaanRepository
from app.core.uow import UnitOfWork


class TabungService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TabungRepository(db)
        self.link_repo = TabungPemeriksaanRepository(db)

    def _generate_barcode(self, id_lab: int, id_jenis: int) -> str:
        ts = int(time.time() * 1000) % 1000000
        return f"T{id_lab:04d}-{id_jenis:02d}-{ts:06d}"

    def create_tabung(self, id_pemeriksaan_lab: int, id_jenis_tabung: int) -> Tabung:
        barcode = self._generate_barcode(id_pemeriksaan_lab, id_jenis_tabung)
        tabung = Tabung(
            id_pemeriksaan_lab=id_pemeriksaan_lab,
            id_jenis_tabung=id_jenis_tabung,
            barcode=barcode,
            status="READY",
        )
        self.repo.create(tabung)
        self.db.flush()

        from app.models.barang import Barang, PemakaianBarang
        barang = self.db.query(Barang).filter(Barang.id_jenis_tabung == id_jenis_tabung).first()
        if barang:
            pakai = PemakaianBarang(id_tabung=tabung.id_tabung, id_barang=barang.id_barang, jumlah_pakai=1)
            self.db.add(pakai)

        return tabung

    def link_tabung_ke_pemeriksaan(self, id_tabung: int, id_pemeriksaan_pasien: int):
        link = TabungPemeriksaan(id_tabung=id_tabung, id_pemeriksaan_pasien=id_pemeriksaan_pasien)
        self.link_repo.create(link)

    def ambil_sampel(self, id_tabung: int):
        with UnitOfWork(self.db) as uow:
            tabung = self.repo.get_by_id(id_tabung)
            if not tabung:
                return None
            tabung.waktu_ambil = datetime.now()
            tabung.status = "TERISI"
            return {
                "id_tabung": tabung.id_tabung,
                "barcode": tabung.barcode,
                "waktu_ambil": str(tabung.waktu_ambil),
                "status": tabung.status,
            }

    def scan_barcode(self, barcode: str):
        tabung = self.repo.get_by_barcode(barcode)
        if not tabung:
            return None
        return self._detail_tabung(tabung)

    def get_by_lab(self, id_pemeriksaan_lab: int):
        rows = self.repo.get_by_lab(id_pemeriksaan_lab)
        return [self._detail_tabung(t) for t in rows]

    def get_all(self):
        rows = self.repo.get_all()
        return [self._detail_tabung(t) for t in rows]

    def _detail_tabung(self, tabung: Tabung):
        jenis = self.db.query(JenisTabung).get(tabung.id_jenis_tabung)
        lab = self.db.query(PemeriksaanLab).get(tabung.id_pemeriksaan_lab)
        kunjungan = self.db.query(Kunjungan).get(lab.id_kunjungan) if lab else None
        pasien = self.db.query(Pasien).get(kunjungan.idpasien) if kunjungan else None
        return {
            "id_tabung": tabung.id_tabung,
            "id_pemeriksaan_lab": tabung.id_pemeriksaan_lab,
            "id_jenis_tabung": tabung.id_jenis_tabung,
            "barcode": tabung.barcode,
            "waktu_ambil": str(tabung.waktu_ambil) if tabung.waktu_ambil else None,
            "status": tabung.status,
            "created_at": str(tabung.created_at) if tabung.created_at else None,
            "nama_jenis_tabung": jenis.nama_jenis_tabung if jenis else None,
            "warna": jenis.warna if jenis else None,
            "id_kunjungan": lab.id_kunjungan if lab else None,
            "no_reg_kunjungan": kunjungan.no_reg_kunjungan if kunjungan else None,
            "nama_pasien": pasien.nama if pasien else None,
        }
