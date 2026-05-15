from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class TagihanPasien(Base):
    __tablename__ = "tagihan_pasien"

    id = Column(Integer, primary_key=True)
    id_kunjungan = Column(Integer, ForeignKey("kunjungan.id_kunjungan"), nullable=False)
    tgl_tagihan = Column(DateTime, server_default=func.now())
    total_biaya = Column(Integer, default=0)
    status_tagihan = Column(String(10), default="BELUM")


class TagihanPasienDetail(Base):
    __tablename__ = "tagihan_pasien_detail"

    id = Column(Integer, primary_key=True)
    id_tagihan = Column(Integer, ForeignKey("tagihan_pasien.id"), nullable=False)
    id_pemeriksaan_pasien = Column(Integer, ForeignKey("pemeriksaan_pasien.id"), nullable=False)
    biaya = Column(Integer, default=0)
