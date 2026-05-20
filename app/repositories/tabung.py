from app.models.tabung import Tabung, TabungPemeriksaan


class TabungRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id_tabung: int):
        return self.db.query(Tabung).filter(Tabung.id_tabung == id_tabung).first()

    def get_by_barcode(self, barcode: str):
        return self.db.query(Tabung).filter(Tabung.barcode == barcode).first()

    def get_by_lab(self, id_pemeriksaan_lab: int):
        return self.db.query(Tabung).filter(
            Tabung.id_pemeriksaan_lab == id_pemeriksaan_lab
        ).order_by(Tabung.created_at.asc()).all()

    def get_all(self):
        return self.db.query(Tabung).order_by(Tabung.created_at.desc()).all()


class TabungPemeriksaanRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_tabung(self, id_tabung: int):
        return self.db.query(TabungPemeriksaan).filter(
            TabungPemeriksaan.id_tabung == id_tabung
        ).all()

    def get_by_pemeriksaan_pasien(self, id_pemeriksaan_pasien: int):
        return self.db.query(TabungPemeriksaan).filter(
            TabungPemeriksaan.id_pemeriksaan_pasien == id_pemeriksaan_pasien
        ).first()

    def get_tabung_by_pemeriksaan_pasien(self, id_pemeriksaan_pasien: int):
        tp = self.get_by_pemeriksaan_pasien(id_pemeriksaan_pasien)
        if not tp:
            return None
        return self.db.query(Tabung).filter(Tabung.id_tabung == tp.id_tabung).first()
