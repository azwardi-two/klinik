from sqlalchemy import func
from app.models.kunjungan import Kunjungan
from app.models.pasien import Pasien


class KunjunganRepository:
    def __init__(self, db):
        self.db = db

    def create(self, kunjungan):
        self.db.add(kunjungan)
        return kunjungan

    def get_all(self, tgl_awal, tgl_akhir, page=1, limit=10):
        offset = (page - 1) * limit

        total = (
            self.db.query(func.count(Kunjungan.id_kunjungan))
            .filter(Kunjungan.tgl_kunjungan.between(tgl_awal, tgl_akhir))
            .scalar()
        )

        if total == 0:
            return 0, []

        rows = (
            self.db.query(
                Kunjungan.tgl_kunjungan,
                Kunjungan.no_reg_kunjungan,
                Pasien.nama,
                Kunjungan.keluhan,
                Kunjungan.status,
            )
            .join(Pasien, Kunjungan.idpasien == Pasien.id)
            .filter(Kunjungan.tgl_kunjungan.between(tgl_awal, tgl_akhir))
            .order_by(Kunjungan.tgl_kunjungan.desc(), Kunjungan.id_kunjungan.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return total, rows