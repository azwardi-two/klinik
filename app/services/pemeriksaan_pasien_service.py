from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.pemeriksaan_lab import PemeriksaanLab
from app.models.kunjungan import Kunjungan
from app.models.pemeriksaan import Pemeriksaan
from app.models.paket_pemeriksaan import PaketPemeriksaan, PaketPemeriksaanDetail
from app.models.hasil_pemeriksaan import HasilPemeriksaan
from app.models.pemeriksaan_jenis_tabung import PemeriksaanJenisTabung
from app.models.tabung import Tabung
from app.repositories.pemeriksaan_pasien import PemeriksaanPasienRepository
from app.repositories.pemeriksaan_lab import PemeriksaanLabRepository
from app.repositories.hasil_pemeriksaan import HasilPemeriksaanRepository
from app.services.tabung_service import TabungService
from app.core.uow import UnitOfWork


class PemeriksaanPasienService:
    def __init__(self, db: Session):
        self.db = db

    def _get_or_create_lab(self, id_kunjungan: int, current_user_id: int):
        lab_repo = PemeriksaanLabRepository(self.db)
        lab = lab_repo.get_by_kunjungan(id_kunjungan)
        if lab:
            return lab

        lab = PemeriksaanLab(
            id_kunjungan=id_kunjungan,
            status="REGISTER",
            created_by=current_user_id,
        )
        lab_repo.create(lab)
        self.db.flush()
        return lab

    def _get_total_lama_waktu(self, rows):
        total_menit = 0
        for pp in rows:
            if pp.jenis == "SATUAN" and pp.id_pemeriksaan:
                pemeriksaan = self.db.query(Pemeriksaan).get(pp.id_pemeriksaan)
                if pemeriksaan:
                    total_menit += pemeriksaan.lama_waktu or 0
            elif pp.jenis == "PAKET" and pp.id_paket:
                details = self.db.query(PaketPemeriksaanDetail).filter(
                    PaketPemeriksaanDetail.id_paket == pp.id_paket
                ).all()
                for detail in details:
                    pemeriksaan = self.db.query(Pemeriksaan).get(detail.id_pemeriksaan)
                    if pemeriksaan:
                        total_menit += pemeriksaan.lama_waktu or 0
        return total_menit

    def _sync_lab_target(self, lab):
        if lab.status != "MULAI" or not lab.jam_mulai:
            return

        rows = PemeriksaanPasienRepository(self.db).get_by_lab(lab.id_pemeriksaan_lab)
        lab.jam_target = lab.jam_mulai + timedelta(minutes=self._get_total_lama_waktu(rows))
        for pp in rows:
            if pp.status != "SELESAI":
                pp.jam_seharusnya_selesai = lab.jam_target

    def add_pemeriksaan(self, id_kunjungan: int, data, current_user_id: int):
        kunjungan = self.db.query(Kunjungan).get(id_kunjungan)
        if not kunjungan:
            raise Exception("Kunjungan tidak ditemukan")

        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            hasil_repo = HasilPemeriksaanRepository(self.db)
            lab = self._get_or_create_lab(id_kunjungan, current_user_id)
            results = []

            for item in data.items:
                if item.jenis == "SATUAN":
                    if not item.id_pemeriksaan:
                        raise Exception("id_pemeriksaan wajib untuk jenis SATUAN")

                    pemeriksaan = self.db.query(Pemeriksaan).get(item.id_pemeriksaan)
                    if not pemeriksaan:
                        raise Exception(f"Pemeriksaan id {item.id_pemeriksaan} tidak ditemukan")

                    pp = PemeriksaanPasien(
                        id_pemeriksaan_lab=lab.id_pemeriksaan_lab,
                        id_kunjungan=id_kunjungan,
                        jenis="SATUAN",
                        id_pemeriksaan=item.id_pemeriksaan,
                        biaya_dibebankan=pemeriksaan.biaya,
                        status="PROSES" if lab.status == "MULAI" else "ORDER",
                        jam_mulai=lab.jam_mulai if lab.status == "MULAI" else None,
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
                        "id_pemeriksaan_lab": lab.id_pemeriksaan_lab,
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
                        id_pemeriksaan_lab=lab.id_pemeriksaan_lab,
                        id_kunjungan=id_kunjungan,
                        jenis="PAKET",
                        id_paket=item.id_paket,
                        biaya_dibebankan=paket.biaya_paket,
                        status="PROSES" if lab.status == "MULAI" else "ORDER",
                        jam_mulai=lab.jam_mulai if lab.status == "MULAI" else None,
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
                        "id_pemeriksaan_lab": lab.id_pemeriksaan_lab,
                        "jenis": "PAKET",
                        "id_paket": item.id_paket,
                        "biaya_dibebankan": paket.biaya_paket,
                        "detail_pemeriksaan_ids": detail_ids,
                    })

                else:
                    raise Exception(f"Jenis '{item.jenis}' tidak valid")

            self._sync_lab_target(lab)

            tabung_service = TabungService(self.db)
            for item in data.items:
                if item.jenis == "SATUAN":
                    mappings = self.db.query(PemeriksaanJenisTabung).filter(
                        PemeriksaanJenisTabung.id_pemeriksaan == item.id_pemeriksaan
                    ).all()
                    for m in mappings:
                        tabung = self.db.query(Tabung).filter(
                            Tabung.id_pemeriksaan_lab == lab.id_pemeriksaan_lab,
                            Tabung.id_jenis_tabung == m.id_jenis_tabung,
                            Tabung.status != "SELESAI"
                        ).first()
                        if not tabung:
                            tabung = tabung_service.create_tabung(lab.id_pemeriksaan_lab, m.id_jenis_tabung)
                        pp_id = None
                        for r in results:
                            if r.get("id_pemeriksaan") == item.id_pemeriksaan:
                                pp_id = r["id"]
                                break
                        if pp_id:
                            tabung_service.link_tabung_ke_pemeriksaan(tabung.id_tabung, pp_id)
                elif item.jenis == "PAKET":
                    paket = self.db.query(PaketPemeriksaan).get(item.id_paket)
                    if paket:
                        details = self.db.query(PaketPemeriksaanDetail).filter(
                            PaketPemeriksaanDetail.id_paket == item.id_paket
                        ).all()
                        pp_id = None
                        for r in results:
                            if r.get("jenis") == "PAKET" and r.get("id_paket") == item.id_paket:
                                pp_id = r["id"]
                                break
                        if pp_id:
                            for d in details:
                                mappings = self.db.query(PemeriksaanJenisTabung).filter(
                                    PemeriksaanJenisTabung.id_pemeriksaan == d.id_pemeriksaan
                                ).all()
                                for m in mappings:
                                    tabung = self.db.query(Tabung).filter(
                                        Tabung.id_pemeriksaan_lab == lab.id_pemeriksaan_lab,
                                        Tabung.id_jenis_tabung == m.id_jenis_tabung,
                                        Tabung.status != "SELESAI"
                                    ).first()
                                    if not tabung:
                                        tabung = tabung_service.create_tabung(lab.id_pemeriksaan_lab, m.id_jenis_tabung)
                                    tabung_service.link_tabung_ke_pemeriksaan(tabung.id_tabung, pp_id)

            return results

    def list_pemeriksaan(self, id_kunjungan: int):
        repo = PemeriksaanPasienRepository(self.db)
        rows = repo.get_by_kunjungan(id_kunjungan)
        result = []
        for r in rows:
            nama_item = None
            if r.jenis == "SATUAN" and r.id_pemeriksaan:
                pemeriksaan = self.db.query(Pemeriksaan).get(r.id_pemeriksaan)
                nama_item = pemeriksaan.nama_pemeriksaan if pemeriksaan else None
            elif r.jenis == "PAKET" and r.id_paket:
                paket = self.db.query(PaketPemeriksaan).get(r.id_paket)
                nama_item = paket.nama_paket if paket else None

            result.append({
                "id": r.id,
                "id_pemeriksaan_lab": r.id_pemeriksaan_lab,
                "id_kunjungan": r.id_kunjungan,
                "jenis": r.jenis,
                "id_pemeriksaan": r.id_pemeriksaan,
                "id_paket": r.id_paket,
                "nama_item": nama_item,
                "biaya_dibebankan": r.biaya_dibebankan,
                "jam_mulai": str(r.jam_mulai) if r.jam_mulai else None,
                "jam_selesai": str(r.jam_selesai) if r.jam_selesai else None,
                "jam_seharusnya_selesai": str(r.jam_seharusnya_selesai) if r.jam_seharusnya_selesai else None,
                "status": r.status,
            })
        return result

    def mulai_pemeriksaan_lab(self, id_kunjungan: int, current_user_id: int):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            kunjungan = self.db.query(Kunjungan).get(id_kunjungan)
            if not kunjungan:
                return None

            lab = self._get_or_create_lab(id_kunjungan, current_user_id)
            rows = repo.get_by_lab(lab.id_pemeriksaan_lab)
            if not rows:
                rows = repo.get_by_kunjungan(id_kunjungan)
                for pp in rows:
                    pp.id_pemeriksaan_lab = lab.id_pemeriksaan_lab

            if not rows:
                raise Exception("Belum ada pemeriksaan untuk kunjungan ini")

            now = datetime.now()
            if lab.status == "SELESAI":
                raise Exception("Pemeriksaan lab sudah selesai")

            if not lab.jam_mulai:
                lab.jam_mulai = now

            lab.status = "MULAI"
            lab.jam_target = lab.jam_mulai + timedelta(minutes=self._get_total_lama_waktu(rows))
            lab.jam_selesai = None

            for pp in rows:
                if pp.status != "SELESAI":
                    pp.status = "PROSES"
                    pp.jam_mulai = lab.jam_mulai
                    pp.jam_seharusnya_selesai = lab.jam_target

            return {
                "id_pemeriksaan_lab": lab.id_pemeriksaan_lab,
                "id_kunjungan": lab.id_kunjungan,
                "jam_mulai": str(lab.jam_mulai) if lab.jam_mulai else None,
                "jam_target": str(lab.jam_target) if lab.jam_target else None,
                "status": lab.status,
                "jumlah_detail": len(rows),
            }

    def mulai_pemeriksaan(self, id: int, current_user_id: int = None):
        repo = PemeriksaanPasienRepository(self.db)
        pp = repo.get_by_id(id)
        if not pp:
            return None
        return self.mulai_pemeriksaan_lab(pp.id_kunjungan, current_user_id or pp.created_by)

    def selesai_pemeriksaan(self, id: int):
        with UnitOfWork(self.db) as uow:
            repo = PemeriksaanPasienRepository(self.db)
            pp = repo.get_by_id(id)
            if not pp:
                return None

            pp.jam_selesai = datetime.now()
            pp.status = "SELESAI"
            lab = None
            if pp.id_pemeriksaan_lab:
                lab = PemeriksaanLabRepository(self.db).get_by_id(pp.id_pemeriksaan_lab)
                rows = repo.get_by_lab(pp.id_pemeriksaan_lab)
                if rows and all(row.status == "SELESAI" for row in rows):
                    lab.status = "SELESAI"
                    lab.jam_selesai = pp.jam_selesai

            return {
                "id": pp.id,
                "id_pemeriksaan_lab": pp.id_pemeriksaan_lab,
                "jam_selesai": str(pp.jam_selesai),
                "status": pp.status,
                "status_lab": lab.status if lab else None,
            }

    def selesai_pemeriksaan_lab(self, id_kunjungan: int):
        with UnitOfWork(self.db) as uow:
            lab = PemeriksaanLabRepository(self.db).get_by_kunjungan(id_kunjungan)
            if not lab:
                return None

            rows = PemeriksaanPasienRepository(self.db).get_by_lab(lab.id_pemeriksaan_lab)
            if not rows:
                rows = PemeriksaanPasienRepository(self.db).get_by_kunjungan(id_kunjungan)

            if not rows:
                raise Exception("Belum ada pemeriksaan untuk kunjungan ini")

            hasil_repo = HasilPemeriksaanRepository(self.db)
            kurang = []
            for pp in rows:
                hasil_rows = hasil_repo.get_by_pemeriksaan_pasien(pp.id)
                if not hasil_rows or not all(
                    any([
                        h.nilai_bawah is not None,
                        h.nilai_atas is not None,
                        h.nilai_value is not None,
                        bool(h.nilai_text),
                    ])
                    for h in hasil_rows
                ):
                    kurang.append(pp.id)

            if kurang:
                raise Exception("Masih ada hasil pemeriksaan yang belum diisi")

            now = datetime.now()
            lab.status = "SELESAI"
            lab.jam_selesai = lab.jam_selesai or now
            for pp in rows:
                pp.status = "SELESAI"
                pp.jam_selesai = pp.jam_selesai or now

            return {
                "id_pemeriksaan_lab": lab.id_pemeriksaan_lab,
                "id_kunjungan": lab.id_kunjungan,
                "jam_selesai": str(lab.jam_selesai),
                "status": lab.status,
            }
