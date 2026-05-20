from app.models.jenis_tabung import JenisTabung


class JenisTabungRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id_jenis_tabung: int):
        return self.db.query(JenisTabung).filter(JenisTabung.id_jenis_tabung == id_jenis_tabung).first()

    def get_all(self):
        return self.db.query(JenisTabung).order_by(JenisTabung.nama_jenis_tabung.asc()).all()

    def delete(self, obj):
        self.db.delete(obj)
