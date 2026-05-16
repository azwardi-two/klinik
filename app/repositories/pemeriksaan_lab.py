from app.models.pemeriksaan_lab import PemeriksaanLab


class PemeriksaanLabRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id_pemeriksaan_lab: int):
        return self.db.query(PemeriksaanLab).filter(
            PemeriksaanLab.id_pemeriksaan_lab == id_pemeriksaan_lab
        ).first()

    def get_by_kunjungan(self, id_kunjungan: int):
        return self.db.query(PemeriksaanLab).filter(
            PemeriksaanLab.id_kunjungan == id_kunjungan
        ).first()
