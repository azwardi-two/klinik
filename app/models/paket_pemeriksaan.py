from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class PaketPemeriksaan(Base):
    __tablename__ = "paket_pemeriksaan"

    id_paket = Column(Integer, primary_key=True)
    nama_paket = Column(String(200), nullable=False)
    biaya_paket = Column(Integer, default=0)
    keterangan = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class PaketPemeriksaanDetail(Base):
    __tablename__ = "paket_pemeriksaan_detail"

    id = Column(Integer, primary_key=True)
    id_paket = Column(Integer, ForeignKey("paket_pemeriksaan.id_paket"), nullable=False)
    id_pemeriksaan = Column(Integer, ForeignKey("pemeriksaan.id_pemeriksaan"), nullable=False)
