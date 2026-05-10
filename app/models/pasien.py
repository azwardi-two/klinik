from sqlalchemy import Column, Date, Integer, String
from app.core.database import Base

class Pasien(Base):
    __tablename__ = "pasien"

    id = Column("id_pasien",Integer, primary_key=True, index=True)
    nama = Column(String(100))
    alamat = Column(String(255))
    no_rm = Column(String(20) ,unique=True)
    tgl_lahir = Column(Date)
    jenis_kelamin = Column(String(10))
    no_hp = Column(String(20))
