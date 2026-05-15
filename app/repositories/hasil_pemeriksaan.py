from app.models.hasil_pemeriksaan import HasilPemeriksaan


class HasilPemeriksaanRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id: int):
        return self.db.query(HasilPemeriksaan).filter(HasilPemeriksaan.id == id).first()

    def get_by_pemeriksaan_pasien(self, id_pemeriksaan_pasien: int):
        return self.db.query(HasilPemeriksaan).filter(
            HasilPemeriksaan.id_pemeriksaan_pasien == id_pemeriksaan_pasien
        ).all()
