from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.kunjungan import Kunjungan
from app.models.pemeriksaan import Pemeriksaan
from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.repositories.pemeriksaan_pasien import PemeriksaanPasienRepository
from app.repositories.hasil_pemeriksaan import HasilPemeriksaanRepository
from app.core.uow import UnitOfWork


class PemeriksaanPasienService:
    def __init__(self, db: Session):
        self.db = db

    def add_pemeriksaan(self, id_kunjungan: int, data, current_user_id: int):
        kunjungan = self.db.query(Kunjungan).get(id_kunjungan)
        if not kunjungan:
            raise Exception("Kunjungan tidak ditemukan")

        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            hasil_repo = HasilPemeriksaanRepository(self.db)
            results = []

            for item in data.items:
                if item.jenis == "SATUAN":
                    if not item.id_pemeriksaan:
                        raise Exception("id_pemeriksaan wajib untuk jenis SATUAN")

                    pemeriksaan = self.db.query(Pemeriksaan).get(item.id_pemeriksaan)
                    if not pemeriksaan:
                        raise Exception(f"Pemeriksaan id {item.id_pemeriksaan} tidak ditemukan")

                    pp = PemeriksaanPasien(
                        id_kunjungan=id_kunjungan,
                        jenis="SATUAN",
                        id_pemeriksaan=item.id_pemeriksaan,
                        biaya_dibebankan=pemeriksaan.biaya,
                        status="ORDER",
                        created_by=current_user_id,
                    )
                    repo.create(pp)
                    uow.flush()

                    hasil = HasilPemeriksaan(
                        id_pemeriksaan_pasien=pp.id,
                        id_pemeriksaan=item.id_pemeriksaan,
                    )
                    hasil_repo.create(hasil)

                    results.append({
                        "id": pp.id,
                        "jenis": "SATUAN",
                        "id_pemeriksaan": item.id_pemeriksaan,
                        "biaya_dibebankan": pemeriksaan.biaya,
                    })

                elif item.jenis == "PAKET":
                    if not item.id_paket:
                        raise Exception("id_paket wajib untuk jenis PAKET")

                    paket = self.db.query(PaketPemeriksaan).get(item.id_paket)
                    if not paket:
                        raise Exception(f"Paket id {item.id_paket} tidak ditemukan")

                    details = self.db.query(PaketPemeriksaanDetail).filter(
                        PaketPemeriksaanDetail.id_paket == item.id_paket
                    ).all()

                    if not details:
                        raise Exception(f"Paket id {item.id_paket} tidak memiliki detail")

                    pp = PemeriksaanPasien(
                        id_kunjungan=id_kunjungan,
                        jenis="PAKET",
                        id_paket=item.id_paket,
                        biaya_dibebankan=paket.biaya_paket,
                        status="ORDER",
                        created_by=current_user_id,
                    )
                    repo.create(pp)
                    uow.flush()

                    detail_ids = []
                    for d in details:
                        hasil = HasilPemeriksaan(
                            id_pemeriksaan_pasien=pp.id,
                            id_pemeriksaan=d.id_pemeriksaan,
                        )
                        hasil_repo.create(hasil)
                        detail_ids.append(d.id_pemeriksaan)

                    results.append({
                        "id": pp.id,
                        "jenis": "PAKET",
                        "id_paket": item.id_paket,
                        "biaya_dibebankan": paket.biaya_paket,
                        "detail_pemeriksaan_ids": detail_ids,
                    })

                else:
                    raise Exception(f"Jenis '{item.jenis}' tidak valid")

            return results

    def list_pemeriksaan(self, id_kunjungan: int):
        repo = PemeriksaanPasienRepository(self.db)
        rows = repo.get_by_kunjungan(id_kunjungan)
        return [
            {
                "id": r.id,
                "id_kunjungan": r.id_kunjungan,
                "jenis": r.jenis,
                "id_pemeriksaan": r.id_pemeriksaan,
                "id_paket": r.id_paket,
                "biaya_dibebankan": r.biaya_dibebankan,
                "jam_mulai": str(r.jam_mulai) if r.jam_mulai else None,
                "jam_selesai": str(r.jam_selesai) if r.jam_selesai else None,
                "jam_seharusnya_selesai": str(r.jam_seharusnya_selesai) if r.jam_seharusnya_selesai else None,
                "status": r.status,
            }
            for r in rows
        ]

    def mulai_pemeriksaan(self, id: int):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            pp = repo.get_by_id(id)
            if not pp:
                return None

            now = datetime.now()
            pp.jam_mulai = now
            pp.status = "PROSES"

            if pp.jenis == "SATUAN" and pp.id_pemeriksaan:
                pemeriksaan = self.db.query(Pemeriksaan).get(pp.id_pemeriksaan)
                if pemeriksaan:
                    pp.jam_seharusnya_selesai = now + timedelta(minutes=pemeriksaan.lama_waktu or 0)

            elif pp.jenis == "PAKET" and pp.id_paket:
                details = self.db.query(PaketPemeriksaanDetail).filter(
                    PaketPemeriksaanDetail.id_paket == pp.id_paket
                ).all()
                total_menit = 0
                for d in details:
                    p = self.db.query(Pemeriksaan).get(d.id_pemeriksaan)
                    if p:
                        total_menit += p.lama_waktu or 0
                pp.jam_seharusnya_selesai = now + timedelta(minutes=total_menit)

            return {
                "id": pp.id,
                "jam_mulai": str(pp.jam_mulai),
                "jam_seharusnya_selesai": str(pp.jam_seharusnya_selesai),
                "status": pp.status,
            }

    def selesai_pemeriksaan(self, id: int):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            pp = repo.get_by_id(id)
            if not pp:
                return None

            pp.jam_selesai = datetime.now()
            pp.status = "SELESAI"

            return {
                "id": pp.id,
                "jam_selesai": str(pp.jam_selesai),
                "status": pp.status,
            }
