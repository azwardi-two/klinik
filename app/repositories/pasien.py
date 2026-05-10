class PasienRepository:
    def __init__(self, db):
        self.db = db

    def create(self, pasien):
        self.db.add(pasien)
        return pasien