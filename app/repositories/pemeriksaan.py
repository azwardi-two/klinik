from app.models.pemeriksaan import Pemeriksaan


class PemeriksaanRepository:
    def __init__(self, db):
        self.db = db

    def create(self, pemeriksaan):
        self.db.add(pemeriksaan)
        return pemeriksaan

    def get_by_id(self, id_pemeriksaan: int):
        return self.db.query(Pemeriksaan).filter(Pemeriksaan.id_pemeriksaan == id_pemeriksaan).first()

    def get_all(self):
        return self.db.query(Pemeriksaan).order_by(Pemeriksaan.nama_pemeriksaan.asc()).all()

    def update(self, pemeriksaan):
        self.db.merge(pemeriksaan)
        return pemeriksaan

    def delete(self, pemeriksaan):
        self.db.delete(pemeriksaan)
