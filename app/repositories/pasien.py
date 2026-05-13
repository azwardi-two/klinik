from app.schemas import pasien
from app.models.pasien import Pasien


class PasienRepository:
    def __init__(self, db):
        self.db = db

    def create(self, pasien):
        self.db.add(pasien)
        return pasien
    
    def get_by_id(self, idpasien: int):
        return self.db.query(pasien).filter(pasien.id == idpasien).first()
    
    def search_by_nama(self, nama: str):
        return self.db.query(Pasien).filter(
            Pasien.nama.ilike(f"%{nama}%")
        ).all()