from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey,DateTime
from app.core.database import Base

class Kunjungan(Base):
    __tablename__ = "kunjungan"

    id_kunjungan = Column(Integer, primary_key=True)
    tgl_kunjungan = Column(Date)
    no_reg_kunjungan = Column(String(20))

    idpasien = Column("id_pasien",Integer, ForeignKey("pasien.id_pasien"))

    umur_hari_pasien = Column("umur_hari",Integer)
    jam_registrasi = Column(DateTime)
    jam_mulai = Column(DateTime)
    jam_selesai = Column(DateTime)

    status = Column(String(50))
    keluhan = Column(String(255))