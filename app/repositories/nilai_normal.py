from app.models.nilai_normal import NilaiNormal


class NilaiNormalRepository:
    def __init__(self, db):
        self.db = db

    def create(self, nilai_normal):
        self.db.add(nilai_normal)
        return nilai_normal

    def get_by_id(self, id_nilai_normal: int):
        return self.db.query(NilaiNormal).filter(NilaiNormal.id_nilai_normal == id_nilai_normal).first()

    def get_by_pemeriksaan(self, id_pemeriksaan: int):
        return self.db.query(NilaiNormal).filter(
            NilaiNormal.id_pemeriksaan == id_pemeriksaan
        ).order_by(NilaiNormal.usia_hari_min.asc()).all()

    def get_all(self):
        return self.db.query(NilaiNormal).all()

    def delete(self, nilai_normal):
        self.db.delete(nilai_normal)
