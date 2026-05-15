from app.models.pemeriksaan import Pemeriksaan
from app.repositories.pemeriksaan import PemeriksaanRepository
from app.core.uow import UnitOfWork


class PemeriksaanService:
    def __init__(self, db):
        self.db = db

    def create_pemeriksaan(self, data):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanRepository(self.db)

            pemeriksaan = Pemeriksaan(
                nama_pemeriksaan=data.nama_pemeriksaan,
                biaya=data.biaya or 0,
                lama_waktu=data.lama_waktu or 0,
                kategori=data.kategori,
            )

            repo.create(pemeriksaan)
            uow.flush()

            return {
                "id_pemeriksaan": pemeriksaan.id_pemeriksaan,
                "nama_pemeriksaan": pemeriksaan.nama_pemeriksaan,
                "biaya": pemeriksaan.biaya,
                "lama_waktu": pemeriksaan.lama_waktu,
                "kategori": pemeriksaan.kategori,
            }

    def get_pemeriksaan(self, id_pemeriksaan: int):
        repo = PemeriksaanRepository(self.db)
        p = repo.get_by_id(id_pemeriksaan)
        if not p:
            return None
        return {
            "id_pemeriksaan": p.id_pemeriksaan,
            "nama_pemeriksaan": p.nama_pemeriksaan,
            "biaya": p.biaya,
            "lama_waktu": p.lama_waktu,
            "kategori": p.kategori,
            "created_at": str(p.created_at) if p.created_at else None,
            "updated_at": str(p.updated_at) if p.updated_at else None,
        }

    def get_all_pemeriksaan(self):
        repo = PemeriksaanRepository(self.db)
        rows = repo.get_all()
        return [
            {
                "id_pemeriksaan": r.id_pemeriksaan,
                "nama_pemeriksaan": r.nama_pemeriksaan,
                "biaya": r.biaya,
                "lama_waktu": r.lama_waktu,
                "kategori": r.kategori,
                "created_at": str(r.created_at) if r.created_at else None,
                "updated_at": str(r.updated_at) if r.updated_at else None,
            }
            for r in rows
        ]

    def update_pemeriksaan(self, id_pemeriksaan: int, data):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanRepository(self.db)
            p = repo.get_by_id(id_pemeriksaan)
            if not p:
                return None

            if data.nama_pemeriksaan is not None:
                p.nama_pemeriksaan = data.nama_pemeriksaan
            if data.biaya is not None:
                p.biaya = data.biaya
            if data.lama_waktu is not None:
                p.lama_waktu = data.lama_waktu
            if data.kategori is not None:
                p.kategori = data.kategori

            uow.flush()

            return {
                "id_pemeriksaan": p.id_pemeriksaan,
                "nama_pemeriksaan": p.nama_pemeriksaan,
                "biaya": p.biaya,
                "lama_waktu": p.lama_waktu,
                "kategori": p.kategori,
            }

    def delete_pemeriksaan(self, id_pemeriksaan: int):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanRepository(self.db)
            p = repo.get_by_id(id_pemeriksaan)
            if not p:
                return False
            repo.delete(p)
            return True
