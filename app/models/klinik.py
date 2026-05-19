from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Klinik(Base):
    __tablename__ = "klinik"

    id_klinik = Column(Integer, primary_key=True)
    nama = Column(String(200), nullable=False)
    alamat = Column(Text, nullable=True)
    telepon = Column(String(50), nullable=True)
    logo = Column(String(255), nullable=True)
