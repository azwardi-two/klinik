from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Tabung(Base):
    __tablename__ = "tabung"

    id_tabung = Column(Integer, primary_key=True)
    id_pemeriksaan_lab = Column(Integer, ForeignKey("pemeriksaan_lab.id_pemeriksaan_lab"), nullable=False)
    id_jenis_tabung = Column(Integer, ForeignKey("jenis_tabung.id_jenis_tabung"), nullable=False)
    barcode = Column(String(100), unique=True, nullable=False)
    waktu_ambil = Column(DateTime, nullable=True)
    status = Column(String(20), default="READY")
    created_at = Column(DateTime, server_default=func.now())


class TabungPemeriksaan(Base):
    __tablename__ = "tabung_pemeriksaan"

    id = Column(Integer, primary_key=True)
    id_tabung = Column(Integer, ForeignKey("tabung.id_tabung"), nullable=False)
    id_pemeriksaan_pasien = Column(Integer, ForeignKey("pemeriksaan_pasien.id"), nullable=False)
