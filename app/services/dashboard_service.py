from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.pemeriksaan_pasien import PemeriksaanPasien
from app.models.pemeriksaan_lab import PemeriksaanLab
from app.models.kunjungan import Kunjungan
from app.models.pasien import Pasien


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_overdue(self):
        now = datetime.now()

        rows = (
            self.db.query(
                PemeriksaanLab,
                Kunjungan.no_reg_kunjungan,
                Kunjungan.tgl_kunjungan,
                Pasien.nama,
                Pasien.no_rm,
            )
            .join(Kunjungan, PemeriksaanLab.id_kunjungan == Kunjungan.id_kunjungan)
            .join(Pasien, Kunjungan.idpasien == Pasien.id)
            .filter(
                PemeriksaanLab.status != "SELESAI",
                PemeriksaanLab.jam_target.isnot(None),
                PemeriksaanLab.jam_target < now,
            )
            .order_by(PemeriksaanLab.jam_target.asc())
            .all()
        )

        result = []
        for lab, no_reg, tgl, nama_pasien, no_rm in rows:
            selisih = now - lab.jam_target
            jam = int(selisih.total_seconds() // 3600)
            menit = int((selisih.total_seconds() % 3600) // 60)
            jumlah_detail = self.db.query(PemeriksaanPasien).filter(
                PemeriksaanPasien.id_pemeriksaan_lab == lab.id_pemeriksaan_lab
            ).count()

            result.append({
                "id_pemeriksaan_lab": lab.id_pemeriksaan_lab,
                "id_kunjungan": lab.id_kunjungan,
                "no_reg": no_reg,
                "tgl_kunjungan": str(tgl) if tgl else None,
                "nama_pasien": nama_pasien,
                "no_rm": no_rm,
                "status": lab.status,
                "jam_mulai": str(lab.jam_mulai) if lab.jam_mulai else None,
                "jam_target": str(lab.jam_target) if lab.jam_target else None,
                "jam_selesai": str(lab.jam_selesai) if lab.jam_selesai else None,
                "jumlah_detail": jumlah_detail,
                "terlambat": f"{jam} jam {menit} menit",
                "terlambat_menit": int(selisih.total_seconds() // 60),
            })

        return result

    def get_statistik(self):
        now = datetime.now()
        today = date.today()

        total_hari_ini = (
            self.db.query(PemeriksaanLab)
            .join(Kunjungan, PemeriksaanLab.id_kunjungan == Kunjungan.id_kunjungan)
            .filter(Kunjungan.tgl_kunjungan == today)
            .count()
        )

        total_selesai = (
            self.db.query(PemeriksaanLab)
            .filter(PemeriksaanLab.status == "SELESAI")
            .count()
        )

        total_proses = (
            self.db.query(PemeriksaanLab)
            .filter(PemeriksaanLab.status == "MULAI")
            .count()
        )

        total_order = (
            self.db.query(PemeriksaanLab)
            .filter(PemeriksaanLab.status == "REGISTER")
            .count()
        )

        total_overdue = (
            self.db.query(PemeriksaanLab)
            .filter(
                PemeriksaanLab.status != "SELESAI",
                PemeriksaanLab.jam_target.isnot(None),
                PemeriksaanLab.jam_target < now,
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
