from app.models.barang import Barang, PenerimaanBarang, PemakaianBarang


class BarangRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id_barang: int):
        return self.db.query(Barang).filter(Barang.id_barang == id_barang).first()

    def get_all(self):
        return self.db.query(Barang).order_by(Barang.nama_barang.asc()).all()

    def get_by_kategori(self, kategori: str):
        return self.db.query(Barang).filter(Barang.kategori == kategori).order_by(Barang.nama_barang.asc()).all()

    def get_by_jenis_tabung(self, id_jenis_tabung: int):
        return self.db.query(Barang).filter(Barang.id_jenis_tabung == id_jenis_tabung).first()

    def delete(self, obj):
        self.db.delete(obj)


class PenerimaanBarangRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_barang(self, id_barang: int):
        return self.db.query(PenerimaanBarang).filter(
            PenerimaanBarang.id_barang == id_barang
        ).order_by(PenerimaanBarang.created_at.desc()).all()


class PemakaianBarangRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_barang(self, id_barang: int):
        return self.db.query(PemakaianBarang).filter(
            PemakaianBarang.id_barang == id_barang
        ).order_by(PemakaianBarang.created_at.desc()).all()

    def get_by_tabung(self, id_tabung: int):
        return self.db.query(PemakaianBarang).filter(
            PemakaianBarang.id_tabung == id_tabung
        ).all()
