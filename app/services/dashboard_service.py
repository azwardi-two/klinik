from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.kunjungan import Kunjungan
from app.models.pasien import Pasien
from app.models.pemeriksaan import Pemeriksaan
from app.models.paket_pemeriksaan import PaketPemeriksaan


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_overdue(self):
        now = datetime.now()

        rows = (
            self.db.query(
                PemeriksaanPasien,
                Kunjungan.no_reg_kunjungan,
                Kunjungan.tgl_kunjungan,
                Pasien.nama,
                Pasien.no_rm,
            )
            .join(Kunjungan, PemeriksaanPasien.id_kunjungan == Kunjungan.id_kunjungan)
            .join(Pasien, Kunjungan.idpasien == Pasien.id)
            .filter(
                PemeriksaanPasien.status.in_(["ORDER", "PROSES"]),
                PemeriksaanPasien.jam_seharusnya_selesai.isnot(None),
                PemeriksaanPasien.jam_seharusnya_selesai < now,
            )
            .order_by(PemeriksaanPasien.jam_seharusnya_selesai.asc())
            .all()
        )

        result = []
        for pp, no_reg, tgl, nama_pasien, no_rm in rows:
            selisih = now - pp.jam_seharusnya_selesai
            jam = int(selisih.total_seconds() // 3600)
            menit = int((selisih.total_seconds() % 3600) // 60)

            nama_item = None
            if pp.jenis == "SATUAN" and pp.id_pemeriksaan:
                p = self.db.query(Pemeriksaan).get(pp.id_pemeriksaan)
                nama_item = p.nama_pemeriksaan if p else None
            elif pp.jenis == "PAKET" and pp.id_paket:
                p = self.db.query(PaketPemeriksaan).get(pp.id_paket)
                nama_item = p.nama_paket if p else None

            result.append({
                "id_pemeriksaan_pasien": pp.id,
                "no_reg": no_reg,
                "tgl_kunjungan": str(tgl) if tgl else None,
                "nama_pasien": nama_pasien,
                "no_rm": no_rm,
                "jenis": pp.jenis,
                "nama_item": nama_item,
                "status": pp.status,
                "jam_mulai": str(pp.jam_mulai) if pp.jam_mulai else None,
                "jam_seharusnya_selesai": str(pp.jam_seharusnya_selesai) if pp.jam_seharusnya_selesai else None,
                "terlambat": f"{jam} jam {menit} menit",
                "terlambat_menit": int(selisih.total_seconds() // 60),
            })

        return result

    def get_statistik(self):
        now = datetime.now()
        today = date.today()

        total_hari_ini = (
            self.db.query(PemeriksaanPasien)
            .join(Kunjungan, PemeriksaanPasien.id_kunjungan == Kunjungan.id_kunjungan)
            .filter(Kunjungan.tgl_kunjungan == today)
            .count()
        )

        total_selesai = (
            self.db.query(PemeriksaanPasien)
            .filter(PemeriksaanPasien.status == "SELESAI")
            .count()
        )

        total_proses = (
            self.db.query(PemeriksaanPasien)
            .filter(PemeriksaanPasien.status == "PROSES")
            .count()
        )

        total_order = (
            self.db.query(PemeriksaanPasien)
            .filter(PemeriksaanPasien.status == "ORDER")
            .count()
        )

        total_overdue = (
            self.db.query(PemeriksaanPasien)
            .filter(
                PemeriksaanPasien.status.in_(["ORDER", "PROSES"]),
                PemeriksaanPasien.jam_seharusnya_selesai.isnot(None),
                PemeriksaanPasien.jam_seharusnya_selesai < now,
            )
            .count()
        )

        return {
            "total_hari_ini": total_hari_ini,
            "total_selesai": total_selesai,
            "total_proses": total_proses,
            "total_order": total_order,
            "total_overdue": total_overdue,
        }
