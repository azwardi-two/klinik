from app.models.pemeriksaan_jenis_tabung import PemeriksaanJenisTabung


class PemeriksaanJenisTabungRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id: int):
        return self.db.query(PemeriksaanJenisTabung).filter(PemeriksaanJenisTabung.id == id).first()

    def get_by_pemeriksaan(self, id_pemeriksaan: int):
        return self.db.query(PemeriksaanJenisTabung).filter(
            PemeriksaanJenisTabung.id_pemeriksaan == id_pemeriksaan
        ).all()

    def get_by_jenis_tabung(self, id_jenis_tabung: int):
        return self.db.query(PemeriksaanJenisTabung).filter(
            PemeriksaanJenisTabung.id_jenis_tabung == id_jenis_tabung
        ).all()

    def get_all(self):
        return self.db.query(PemeriksaanJenisTabung).all()

    def delete(self, obj):
        self.db.delete(obj)

    def delete_by_pemeriksaan(self, id_pemeriksaan: int):
        self.db.query(PemeriksaanJenisTabung).filter(
            PemeriksaanJenisTabung.id_pemeriksaan == id_pemeriksaan
        ).delete()
