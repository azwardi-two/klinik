from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class JenisTabung(Base):
    __tablename__ = "jenis_tabung"

    id_jenis_tabung = Column(Integer, primary_key=True)
    nama_jenis_tabung = Column(String(100), nullable=False)
    warna = Column(String(50))
    volume_ml = Column(Float)
    keterangan = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
