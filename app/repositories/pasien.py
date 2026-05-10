from app.schemas import pasien


class PasienRepository:
    def __init__(self, db):
        self.db = db

    def create(self, pasien):
        self.db.add(pasien)
        return pasien
    
    def get_by_id(self, idpasien: int):
        return self.db.query(pasien).filter(pasien.id == idpasien).first()