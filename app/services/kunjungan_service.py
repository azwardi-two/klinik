from datetime import datetime, date
from app.models.pasien import Pasien
from app.models.kunjungan import Kunjungan
from app.models.user import User
from app.repositories.pasien import PasienRepository
from app.repositories.kunjungan import KunjunganRepository
from app.services.counter_service import CounterService
from app.core.uow import UnitOfWork


class KunjunganService:
    def __init__(self, db):
        self.db = db

    def create_kunjungan(self, data, current_user: User):
        with UnitOfWork(self.db) as uow:
            pasien_repo = PasienRepository(self.db)
            kunjungan_repo = KunjunganRepository(self.db)
            counter = CounterService(self.db)

            tgl_kunjungan = data.tgl_kunjungan
            umur_hari = None

            if data.idpasien:
                pasien = self.db.query(Pasien).get(data.idpasien)
                if not pasien:
                    raise Exception(f"Pasien dengan id {data.idpasien} tidak ditemukan")
                no_rm = pasien.no_rm
                umur_hari = (tgl_kunjungan - pasien.tgl_lahir).days
            else:
                no_rm = counter.generate_no_rm()
                pasien = Pasien(
                    nama=data.nama,
                    tgl_lahir=data.tgl_lahir,
                    jenis_kelamin=data.jenis_kelamin,
                    alamat=data.alamat,
                    no_rm=no_rm,
                    no_hp=data.no_hp,
                )
                pasien_repo.create(pasien)
                uow.flush()

            no_reg = counter.generate_no_reg()
            umur_hari = (tgl_kunjungan - pasien.tgl_lahir).days

            kunjungan = Kunjungan(
                tgl_kunjungan=datetime.now().date(),
                no_reg_kunjungan=no_reg,
                idpasien=pasien.id,
                umur_hari_pasien=umur_hari,
                jam_registrasi=datetime.now(),
                jam_mulai=datetime.now(),
                status="ORDER",
                keluhan=data.keluhan,
                created_by=current_user.id,
            )

            kunjungan_repo.create(kunjungan)

            return {
                "idpasien": pasien.id,
                "no_rm": no_rm,

            }

    def get_all_kunjungan(self, tgl_awal: date, tgl_akhir: date, page: int = 1, limit: int = 10):
        repo = KunjunganRepository(self.db)
        total, rows = repo.get_all(tgl_awal, tgl_akhir, page, limit)

        data = [
            {
                "id_kunjungan": r.id_kunjungan,
                "tgl_kunjungan": r.tgl_kunjungan,
                "no_reg": r.no_reg_kunjungan,
                "nama_pasien": r.nama,
                "keluhan": r.keluhan,
                "status": r.status,
            }
            for r in rows
        ]

        total_pages = max(1, (total + limit - 1) // limit)

        return {
            "data": data,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
        }
        
