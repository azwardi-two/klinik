from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base


class Pemeriksaan(Base):
    __tablename__ = "pemeriksaan"

    id_pemeriksaan = Column(Integer, primary_key=True)
    nama_pemeriksaan = Column(String(200), nullable=False)
    biaya = Column(Integer, default=0)
    lama_waktu = Column(Integer, default=0)
    kategori = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
