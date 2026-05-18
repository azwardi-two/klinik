from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.core.database import Base


class NilaiNormal(Base):
    __tablename__ = "nilai_normal"

    id_nilai_normal = Column(Integer, primary_key=True)
    id_pemeriksaan = Column(Integer, ForeignKey("pemeriksaan.id_pemeriksaan"), nullable=False)
    jenis_kelamin = Column(String(1), nullable=True)
    usia_hari_min = Column(Integer, default=0)
    usia_hari_max = Column(Integer, default=99999)
    nilai_bawah = Column(Float, nullable=True)
    nilai_atas = Column(Float, nullable=True)
    operator = Column(String(2), nullable=True)
    nilai_operator = Column(Float, nullable=True)
    nilai_text = Column(Text, nullable=True)
    keterangan = Column(String(255), nullable=True)
