from sqlalchemy.orm import Session
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.models.kunjungan import Kunjungan
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.pasien import Pasien
from app.repositories.hasil_pemeriksaan import HasilPemeriksaanRepository
from app.services.nilai_normal_service import NilaiNormalService
from app.core.uow import UnitOfWork


class HasilPemeriksaanService:
    def __init__(self, db: Session):
        self.db = db

    def get_hasil_by_pemeriksaan_pasien(self, id_pemeriksaan_pasien: int):
        repo = HasilPemeriksaanRepository(self.db)
        rows = repo.get_by_pemeriksaan_pasien(id_pemeriksaan_pasien)
        return [
            {
                "id": r.id,
                "id_pemeriksaan_pasien": r.id_pemeriksaan_pasien,
                "id_pemeriksaan": r.id_pemeriksaan,
                "nilai_bawah": r.nilai_bawah,
                "nilai_atas": r.nilai_atas,
                "nilai_value": r.nilai_value,
                "nilai_text": r.nilai_text,
                "status_nilai": r.status_nilai,
                "keterangan": r.keterangan,
            }
            for r in rows
        ]

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

                    nilai_svc = NilaiNormalService(self.db)
                    status = nilai_svc.compute_status_nilai(
                        id_pemeriksaan=hasil.id_pemeriksaan,
                        nilai_bawah=hasil.nilai_bawah,
                        nilai_atas=hasil.nilai_atas,
                        nilai_value=hasil.nilai_value,
                        nilai_text=hasil.nilai_text,
                        jenis_kelamin=jenis_kelamin,
                        umur_hari=umur_hari,
                    )
                    hasil.status_nilai = status

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
