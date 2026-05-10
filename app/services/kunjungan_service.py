from datetime import datetime
from app.models.pasien import Pasien
from app.models.kunjungan import Kunjungan
from app.repositories.pasien import PasienRepository
from app.repositories.kunjungan import KunjunganRepository
from app.services.counter_service import CounterService
from app.core.uow import UnitOfWork


class KunjunganService:
    def __init__(self, db):
        self.db = db

    def create_kunjungan(self, data):
        with UnitOfWork(self.db) as uow:
            pasien_repo = PasienRepository(self.db)
            kunjungan_repo = KunjunganRepository(self.db)
            counter = CounterService(self.db)

        # 🔹 CEK: pakai pasien lama atau baru
        if data.idpasien:
            pasien = self.db.query(Pasien).get(data.idpasien)

            if not pasien:
                raise Exception("Pasien tidak ditemukan")

            no_rm = pasien.no_rm

        else:
            # 👉 create pasien baru
            no_rm = counter.generate_no_rm()

            pasien = Pasien(
                nama=data.nama,
                no_rm=no_rm
            )
            pasien_repo.create(pasien)

            uow.flush()

        # 🔹 generate nomor kunjungan
        no_reg = counter.generate_no_reg()

        # 🔹 hitung umur kalau ada tgl_lahir
        umur_hari = getattr(data, "umur_hari", None)

        kunjungan = Kunjungan(
            tgl_kunjungan=datetime.now().date(),
            no_reg_kunjungan=no_reg,
            idpasien=pasien.id,
            umur_hari_pasien=umur_hari,
            jam_registrasi=datetime.now().time(),
            status="registrasi",
            keluhan=data.keluhan
        )

        kunjungan_repo.create(kunjungan)

        return {
            "idpasien": pasien.id,
            "no_rm": no_rm,
            "no_reg": no_reg
        }