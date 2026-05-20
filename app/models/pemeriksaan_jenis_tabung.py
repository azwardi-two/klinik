from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class PemeriksaanJenisTabung(Base):
    __tablename__ = "pemeriksaan_jenis_tabung"

    id = Column(Integer, primary_key=True)
    id_pemeriksaan = Column(Integer, ForeignKey("pemeriksaan.id_pemeriksaan"), nullable=False)
    id_jenis_tabung = Column(Integer, ForeignKey("jenis_tabung.id_jenis_tabung"), nullable=False)
    jumlah_tabung = Column(Integer, default=1)
