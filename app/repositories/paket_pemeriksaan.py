from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail


class PaketPemeriksaanRepository:
    def __init__(self, db):
        self.db = db

    def create(self, paket):
        self.db.add(paket)
        return paket

    def get_by_id(self, id_paket: int):
        return self.db.query(PaketPemeriksaan).filter(PaketPemeriksaan.id_paket == id_paket).first()

    def get_all(self):
        return self.db.query(PaketPemeriksaan).order_by(PaketPemeriksaan.nama_paket.asc()).all()

    def delete(self, paket):
        self.db.delete(paket)


class PaketPemeriksaanDetailRepository:
    def __init__(self, db):
        self.db = db

    def create(self, detail):
        self.db.add(detail)
        return detail

    def get_by_paket(self, id_paket: int):
        return self.db.query(PaketPemeriksaanDetail).filter(
            PaketPemeriksaanDetail.id_paket == id_paket
        ).all()

    def delete_by_paket(self, id_paket: int):
        self.db.query(PaketPemeriksaanDetail).filter(
            PaketPemeriksaanDetail.id_paket == id_paket
        ).delete()
