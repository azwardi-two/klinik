from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class PemeriksaanPasien(Base):
    __tablename__ = "pemeriksaan_pasien"

    id = Column(Integer, primary_key=True)
    id_kunjungan = Column(Integer, ForeignKey("kunjungan.id_kunjungan"), nullable=False)
    jenis = Column(String(10), nullable=False)
    id_pemeriksaan = Column(Integer, ForeignKey("pemeriksaan.id_pemeriksaan"), nullable=True)
    id_paket = Column(Integer, ForeignKey("paket_pemeriksaan.id_paket"), nullable=True)
    biaya_dibebankan = Column(Integer, default=0)
    jam_mulai = Column(DateTime, nullable=True)
    jam_selesai = Column(DateTime, nullable=True)
    jam_seharusnya_selesai = Column(DateTime, nullable=True)
    status = Column(String(10), default="ORDER")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
