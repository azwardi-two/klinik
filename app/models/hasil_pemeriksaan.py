from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.core.database import Base


class HasilPemeriksaan(Base):
    __tablename__ = "hasil_pemeriksaan"

    id = Column(Integer, primary_key=True)
    id_pemeriksaan_pasien = Column(Integer, ForeignKey("pemeriksaan_pasien.id"), nullable=False)
    id_pemeriksaan = Column(Integer, ForeignKey("pemeriksaan.id_pemeriksaan"), nullable=False)
    nilai_bawah = Column(Float, nullable=True)
    nilai_atas = Column(Float, nullable=True)
    nilai_value = Column(Float, nullable=True)
    nilai_text = Column(Text, nullable=True)
    status_nilai = Column(String(1), nullable=True)
    keterangan = Column(Text, nullable=True)
