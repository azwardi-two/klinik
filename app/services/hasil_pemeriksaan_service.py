from datetime import datetime
from sqlalchemy.orm import Session
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.models.kunjungan import Kunjungan
from app.models.nilai_normal import NilaiNormal
from app.models.pemeriksaan import Pemeriksaan
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.pemeriksaan_lab import PemeriksaanLab
from app.models.pasien import Pasien
from app.repositories.hasil_pemeriksaan import HasilPemeriksaanRepository
from app.services.nilai_normal_service import NilaiNormalService
from app.core.uow import UnitOfWork


class HasilPemeriksaanService:
    def __init__(self, db: Session):
        self.db = db

    def _hasil_sudah_diisi(self, hasil):
        return any([
            hasil.nilai_bawah is not None,
            hasil.nilai_atas is not None,
            hasil.nilai_value is not None,
            bool(hasil.nilai_text),
        ])

    def _sync_status_selesai(self, pp):
        rows = HasilPemeriksaanRepository(self.db).get_by_pemeriksaan_pasien(pp.id)
        if rows and all(self._hasil_sudah_diisi(row) for row in rows):
            now = datetime.now()
            pp.status = "SELESAI"
            pp.jam_selesai = pp.jam_selesai or now

            if pp.id_pemeriksaan_lab:
                lab_rows = self.db.query(PemeriksaanPasien).filter(
                    PemeriksaanPasien.id_pemeriksaan_lab == pp.id_pemeriksaan_lab
                ).all()
                if lab_rows and all(row.status == "SELESAI" for row in lab_rows):
                    lab = self.db.query(PemeriksaanLab).get(pp.id_pemeriksaan_lab)
                    if lab:
                        lab.status = "SELESAI"
                        lab.jam_selesai = lab.jam_selesai or now

    def _get_nilai_normal_match(self, id_pemeriksaan, jenis_kelamin=None, umur_hari=None):
        rows = self.db.query(NilaiNormal).filter(
            NilaiNormal.id_pemeriksaan == id_pemeriksaan
        ).all()
        for n in rows:
            if n.jenis_kelamin and jenis_kelamin and n.jenis_kelamin != jenis_kelamin:
                continue
            if umur_hari is not None and not (n.usia_hari_min <= umur_hari <= n.usia_hari_max):
                continue
            return n
        return rows[0] if rows else None

    def _format_nilai_normal(self, n, jenis_nilai):
        if not n:
            return None
        if jenis_nilai == "range":
            bawah = f"{n.nilai_bawah:g}" if n.nilai_bawah is not None else "-"
            atas = f"{n.nilai_atas:g}" if n.nilai_atas is not None else "-"
            return f"{bawah} - {atas}"
        if jenis_nilai == "operator":
            return f"{n.operator or ''} {n.nilai_operator:g}".strip() if n.nilai_operator is not None else n.operator
        if jenis_nilai == "text":
            return n.nilai_text
        return None

    def get_hasil_by_pemeriksaan_pasien(self, id_pemeriksaan_pasien: int):
        repo = HasilPemeriksaanRepository(self.db)
        rows = repo.get_by_pemeriksaan_pasien(id_pemeriksaan_pasien)
        pp = self.db.query(PemeriksaanPasien).get(id_pemeriksaan_pasien)
        jenis_kelamin = None
        umur_hari = None
        if pp:
            kunjungan = self.db.query(Kunjungan).get(pp.id_kunjungan)
            if kunjungan:
                umur_hari = kunjungan.umur_hari_pasien
                pasien = self.db.query(Pasien).get(kunjungan.idpasien)
                jenis_kelamin = pasien.jenis_kelamin if pasien else None

        result = []
        for r in rows:
            pemeriksaan = self.db.query(Pemeriksaan).get(r.id_pemeriksaan)
            normal = self._get_nilai_normal_match(r.id_pemeriksaan, jenis_kelamin, umur_hari)
            jenis_nilai = pemeriksaan.jenis_nilai if pemeriksaan else "range"
            result.append({
                "id": r.id,
                "id_pemeriksaan_pasien": r.id_pemeriksaan_pasien,
                "id_pemeriksaan": r.id_pemeriksaan,
                "nama_pemeriksaan": pemeriksaan.nama_pemeriksaan if pemeriksaan else None,
                "satuan": pemeriksaan.satuan if pemeriksaan else None,
                "nilai_bawah": r.nilai_bawah,
                "nilai_atas": r.nilai_atas,
                "nilai_value": r.nilai_value,
                "nilai_text": r.nilai_text,
                "status_nilai": r.status_nilai,
                "keterangan": r.keterangan,
                "nilai_normal": {
                    "jenis_nilai": jenis_nilai,
                    "nilai_bawah": normal.nilai_bawah,
                    "nilai_atas": normal.nilai_atas,
                    "operator": normal.operator,
                    "nilai_operator": normal.nilai_operator,
                    "nilai_text": normal.nilai_text,
                    "keterangan": normal.keterangan,
                    "label": self._format_nilai_normal(normal, jenis_nilai),
                } if normal else None,
            })
        return result

    def update_hasil(self, id_hasil: int, data):
        with UnitOfWork(self.db) as uow:
            repo = HasilPemeriksaanRepository(self.db)
            hasil = repo.get_by_id(id_hasil)
            if not hasil:
                return None

            if data.nilai_bawah is not None and data.nilai_atas is not None:
                hasil.nilai_bawah = data.nilai_bawah
                hasil.nilai_atas = data.nilai_atas
            elif data.nilai_bawah is not None:
                hasil.nilai_bawah = data.nilai_bawah
                hasil.nilai_atas = data.nilai_bawah
            elif data.nilai_atas is not None:
                hasil.nilai_atas = data.nilai_atas
                hasil.nilai_bawah = data.nilai_atas

            if data.nilai_value is not None:
                hasil.nilai_value = data.nilai_value
            if data.nilai_text is not None:
                hasil.nilai_text = data.nilai_text
            if data.keterangan is not None:
                hasil.keterangan = data.keterangan

            pp = self.db.query(PemeriksaanPasien).get(hasil.id_pemeriksaan_pasien)
            if pp:
                kunjungan = self.db.query(Kunjungan).get(pp.id_kunjungan)
                if kunjungan:
                    pasien = self.db.query(Pasien).get(kunjungan.idpasien)
                    umur_hari = kunjungan.umur_hari_pasien
                    jenis_kelamin = pasien.jenis_kelamin if pasien else None

                    pemeriksaan = self.db.query(Pemeriksaan).get(hasil.id_pemeriksaan)
                    jenis_nilai = pemeriksaan.jenis_nilai if pemeriksaan else "range"

                    nilai_svc = NilaiNormalService(self.db)
                    status = nilai_svc.compute_status_nilai(
                        id_pemeriksaan=hasil.id_pemeriksaan,
                        jenis_nilai=jenis_nilai,
                        nilai_bawah=hasil.nilai_bawah,
                        nilai_atas=hasil.nilai_atas,
                        nilai_value=hasil.nilai_value,
                        nilai_text=hasil.nilai_text,
                        jenis_kelamin=jenis_kelamin,
                        umur_hari=umur_hari,
                    )
                    hasil.status_nilai = status
                self._sync_status_selesai(pp)

            return {
                "id": hasil.id,
                "id_pemeriksaan_pasien": hasil.id_pemeriksaan_pasien,
                "id_pemeriksaan": hasil.id_pemeriksaan,
                "nilai_bawah": hasil.nilai_bawah,
                "nilai_atas": hasil.nilai_atas,
                "nilai_value": hasil.nilai_value,
                "nilai_text": hasil.nilai_text,
                "status_nilai": hasil.status_nilai,
                "keterangan": hasil.keterangan,
            }
