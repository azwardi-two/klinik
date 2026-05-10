class KunjunganRepository:
    def __init__(self, db):
        self.db = db

    def create(self, kunjungan):
        self.db.add(kunjungan)
        return kunjungan