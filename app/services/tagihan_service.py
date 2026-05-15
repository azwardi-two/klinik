from sqlalchemy.orm import Session
from app.models.tagihan import TagihanPasien, TagihanPasienDetail
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.repositories.tagihan import TagihanRepository, TagihanDetailRepository
from app.repositories.pemeriksaan_pasien import PemeriksaanPasienRepository
from app.core.uow import UnitOfWork


class TagihanService:
    def __init__(self, db: Session):
        self.db = db

    def generate_tagihan(self, id_kunjungan: int):
        existing = TagihanRepository(self.db).get_by_kunjungan(id_kunjungan)
        if existing:
            raise Exception("Tagihan sudah pernah dibuat untuk kunjungan ini")

        pp_repo = PemeriksaanPasienRepository(self.db)
        items = pp_repo.get_by_kunjungan(id_kunjungan)

        if not items:
            raise Exception("Tidak ada pemeriksaan untuk ditagih")

        with UnitOfWork(self.db) as uow:
            total = sum(item.biaya_dibebankan or 0 for item in items)

            tagihan = TagihanPasien(
                id_kunjungan=id_kunjungan,
                total_biaya=total,
                status_tagihan="BELUM",
            )
            TagihanRepository(self.db).create(tagihan)
            uow.flush()

            detail_repo = TagihanDetailRepository(self.db)
            for item in items:
                detail = TagihanPasienDetail(
                    id_tagihan=tagihan.id,
                    id_pemeriksaan_pasien=item.id,
                    biaya=item.biaya_dibebankan or 0,
                )
                detail_repo.create(detail)

            return {
                "id": tagihan.id,
                "id_kunjungan": tagihan.id_kunjungan,
                "total_biaya": tagihan.total_biaya,
                "status_tagihan": tagihan.status_tagihan,
                "tgl_tagihan": str(tagihan.tgl_tagihan) if tagihan.tgl_tagihan else None,
            }

    def get_tagihan(self, id_kunjungan: int):
        repo = TagihanRepository(self.db)
        detail_repo = TagihanDetailRepository(self.db)

        tagihan = repo.get_by_kunjungan(id_kunjungan)
        if not tagihan:
            return None

        details = detail_repo.get_by_tagihan(tagihan.id)

        return {
            "id": tagihan.id,
            "id_kunjungan": tagihan.id_kunjungan,
            "tgl_tagihan": str(tagihan.tgl_tagihan) if tagihan.tgl_tagihan else None,
            "total_biaya": tagihan.total_biaya,
            "status_tagihan": tagihan.status_tagihan,
            "details": [
                {
                    "id": d.id,
                    "id_pemeriksaan_pasien": d.id_pemeriksaan_pasien,
                    "biaya": d.biaya,
                }
                for d in details
            ],
        }

    def bayar_tagihan(self, id_tagihan: int):
        with UnitOfWork(self.db) as uow:
            repo = TagihanRepository(self.db)
            tagihan = repo.get_by_id(id_tagihan)
            if not tagihan:
                return None
            if tagihan.status_tagihan == "LUNAS":
                raise Exception("Tagihan sudah lunas")

            tagihan.status_tagihan = "LUNAS"

            return {
                "id": tagihan.id,
                "status_tagihan": tagihan.status_tagihan,
            }
