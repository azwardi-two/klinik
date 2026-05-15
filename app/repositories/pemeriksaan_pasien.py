from app.models.pemeriksaan_pasien import PemeriksaanPasien


class PemeriksaanPasienRepository:
    def __init__(self, db):
        self.db = db

    def create(self, obj):
        self.db.add(obj)
        return obj

    def get_by_id(self, id: int):
        return self.db.query(PemeriksaanPasien).filter(PemeriksaanPasien.id == id).first()

    def get_by_kunjungan(self, id_kunjungan: int):
        return self.db.query(PemeriksaanPasien).filter(
            PemeriksaanPasien.id_kunjungan == id_kunjungan
        ).order_by(PemeriksaanPasien.created_at.asc()).all()

    def get_all_overdue(self):
        from datetime import datetime
        return self.db.query(PemeriksaanPasien).filter(
            PemeriksaanPasien.status.in_(["ORDER", "PROSES"]),
            PemeriksaanPasien.jam_seharusnya_selesai.isnot(None),
            PemeriksaanPasien.jam_seharusnya_selesai < datetime.now(),
        ).all()
