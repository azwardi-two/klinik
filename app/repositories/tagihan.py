from app.models.tagihan import TagihanPasien, TagihanPasienDetail


class TagihanRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id: int):
        return self.db.query(TagihanPasien).filter(TagihanPasien.id == id).first()

    def get_by_kunjungan(self, id_kunjungan: int):
        return self.db.query(TagihanPasien).filter(
            TagihanPasien.id_kunjungan == id_kunjungan
        ).first()


class TagihanDetailRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_tagihan(self, id_tagihan: int):
        return self.db.query(TagihanPasienDetail).filter(
            TagihanPasienDetail.id_tagihan == id_tagihan
        ).all()
