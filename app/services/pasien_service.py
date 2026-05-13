from app.models.pasien import Pasien
from app.services.counter_service import CounterService
from app.core.uow import UnitOfWork
from app.repositories.pasien import PasienRepository


class PasienService:
    def __init__(self, db):
        self.db = db

    def create_pasien(self, data):
        with UnitOfWork(self.db) as uow:
            counter = CounterService(self.db)

            no_rm = counter.generate_no_rm()

            pasien = Pasien(
                nama=data.nama,
                alamat=data.alamat,
                jenis_kelamin=data.jenis_kelamin,
                tgl_lahir=data.tgl_lahir,
                no_hp=data.no_hp,
                no_rm=no_rm
            )

            self.db.add(pasien)

            return {
                "id": pasien.id,
                "no_rm": no_rm
            }


    def search_pasien(self, nama: str):
        repo = PasienRepository(self.db)

        hasil = repo.search_by_nama(nama)

        # optional: validasi / manipulasi data
        return hasil