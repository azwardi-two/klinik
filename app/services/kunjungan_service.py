from datetime import datetime, date
from app.models.pasien import Pasien
from app.models.kunjungan import Kunjungan
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.models.pemeriksaan_lab import PemeriksaanLab
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.tagihan import TagihanPasien, TagihanPasienDetail
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
                "no_reg": no_reg,
                "id_kunjungan": kunjungan.id_kunjungan,

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

    def update_kunjungan(self, id_kunjungan: int, data):
        with UnitOfWork(self.db) as uow:
            kunjungan = self.db.query(Kunjungan).get(id_kunjungan)
            if not kunjungan:
                return None

            if data.keluhan is not None:
                kunjungan.keluhan = data.keluhan
            if data.tgl_kunjungan is not None:
                kunjungan.tgl_kunjungan = data.tgl_kunjungan
            if data.status is not None:
                kunjungan.status = data.status

            return {
                "id_kunjungan": kunjungan.id_kunjungan,
                "tgl_kunjungan": kunjungan.tgl_kunjungan,
                "no_reg": kunjungan.no_reg_kunjungan,
                "keluhan": kunjungan.keluhan,
                "status": kunjungan.status,
            }

    def delete_kunjungan(self, id_kunjungan: int):
        with UnitOfWork(self.db) as uow:
            kunjungan = self.db.query(Kunjungan).get(id_kunjungan)
            if not kunjungan:
                return False

            tagihan_rows = self.db.query(TagihanPasien).filter(
                TagihanPasien.id_kunjungan == id_kunjungan
            ).all()
            for tagihan in tagihan_rows:
                self.db.query(TagihanPasienDetail).filter(
                    TagihanPasienDetail.id_tagihan == tagihan.id
                ).delete(synchronize_session=False)
                self.db.delete(tagihan)

            pemeriksaan_rows = self.db.query(PemeriksaanPasien).filter(
                PemeriksaanPasien.id_kunjungan == id_kunjungan
            ).all()
            for pp in pemeriksaan_rows:
                self.db.query(HasilPemeriksaan).filter(
                    HasilPemeriksaan.id_pemeriksaan_pasien == pp.id
                ).delete(synchronize_session=False)
                self.db.delete(pp)

            self.db.query(PemeriksaanLab).filter(
                PemeriksaanLab.id_kunjungan == id_kunjungan
            ).delete(synchronize_session=False)
            self.db.delete(kunjungan)
            return True
        
