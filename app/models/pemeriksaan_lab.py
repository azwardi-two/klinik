from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class PemeriksaanLab(Base):
    __tablename__ = "pemeriksaan_lab"

    id_pemeriksaan_lab = Column(Integer, primary_key=True)
    id_kunjungan = Column(Integer, ForeignKey("kunjungan.id_kunjungan"), nullable=False)
    status = Column(String(20), default="REGISTER")
    jam_mulai = Column(DateTime, nullable=True)
    jam_target = Column(DateTime, nullable=True)
    jam_selesai = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
