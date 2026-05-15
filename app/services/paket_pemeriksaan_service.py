from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail
from app.repositories.paket_pemeriksaan import PaketPemeriksaanRepository, PaketPemeriksaanDetailRepository
from app.core.uow import UnitOfWork


class PaketPemeriksaanService:
    def __init__(self, db):
        self.db = db

    def create_paket(self, data):
        with UnitOfWork(self.db) as uow:
            repo = PaketPemeriksaanRepository(self.db)
            detail_repo = PaketPemeriksaanDetailRepository(self.db)

            paket = PaketPemeriksaan(
                nama_paket=data.nama_paket,
                biaya_paket=data.biaya_paket or 0,
                keterangan=data.keterangan,
            )

            repo.create(paket)
            uow.flush()

            if data.detail_items:
                for item in data.detail_items:
                    detail = PaketPemeriksaanDetail(
                        id_paket=paket.id_paket,
                        id_pemeriksaan=item.id_pemeriksaan,
                    )
                    detail_repo.create(detail)

            return {
                "id_paket": paket.id_paket,
                "nama_paket": paket.nama_paket,
                "biaya_paket": paket.biaya_paket,
                "keterangan": paket.keterangan,
            }

    def get_paket(self, id_paket: int):
        repo = PaketPemeriksaanRepository(self.db)
        detail_repo = PaketPemeriksaanDetailRepository(self.db)

        p = repo.get_by_id(id_paket)
        if not p:
            return None

        details = detail_repo.get_by_paket(id_paket)

        return {
            "id_paket": p.id_paket,
            "nama_paket": p.nama_paket,
            "biaya_paket": p.biaya_paket,
            "keterangan": p.keterangan,
            "created_at": str(p.created_at) if p.created_at else None,
            "detail_items": [
                {
                    "id": d.id,
                    "id_pemeriksaan": d.id_pemeriksaan,
                }
                for d in details
            ],
        }

    def get_all_paket(self):
        repo = PaketPemeriksaanRepository(self.db)
        detail_repo = PaketPemeriksaanDetailRepository(self.db)

        rows = repo.get_all()
        result = []
        for p in rows:
            details = detail_repo.get_by_paket(p.id_paket)
            result.append({
                "id_paket": p.id_paket,
                "nama_paket": p.nama_paket,
                "biaya_paket": p.biaya_paket,
                "keterangan": p.keterangan,
                "created_at": str(p.created_at) if p.created_at else None,
                "detail_items": [
                    {
                        "id": d.id,
                        "id_pemeriksaan": d.id_pemeriksaan,
                    }
                    for d in details
                ],
            })
        return result

    def update_paket(self, id_paket: int, data):
        with UnitOfWork(self.db) as uow:
            repo = PaketPemeriksaanRepository(self.db)
            detail_repo = PaketPemeriksaanDetailRepository(self.db)

            p = repo.get_by_id(id_paket)
            if not p:
                return None

            if data.nama_paket is not None:
                p.nama_paket = data.nama_paket
            if data.biaya_paket is not None:
                p.biaya_paket = data.biaya_paket
            if data.keterangan is not None:
                p.keterangan = data.keterangan

            if data.detail_items is not None:
                detail_repo.delete_by_paket(id_paket)
                for item in data.detail_items:
                    detail = PaketPemeriksaanDetail(
                        id_paket=id_paket,
                        id_pemeriksaan=item.id_pemeriksaan,
                    )
                    detail_repo.create(detail)

            return {
                "id_paket": p.id_paket,
                "nama_paket": p.nama_paket,
                "biaya_paket": p.biaya_paket,
                "keterangan": p.keterangan,
            }

    def delete_paket(self, id_paket: int):
        with UnitOfWork(self.db) as uow:
            repo = PaketPemeriksaanRepository(self.db)
            detail_repo = PaketPemeriksaanDetailRepository(self.db)

            p = repo.get_by_id(id_paket)
            if not p:
                return False

            detail_repo.delete_by_paket(id_paket)
            repo.delete(p)
            return True
