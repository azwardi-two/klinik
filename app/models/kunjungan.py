from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from app.core.database import Base

class Kunjungan(Base):
    __tablename__ = "kunjungan"

    id_kunjungan = Column(Integer, primary_key=True)
    tgl_kunjungan = Column(Date)
    no_reg_kunjungan = Column(String(20))

    idpasien = Column(Integer, ForeignKey("pasien.id"))

    umur_hari_pasien = Column(Integer)
    jam_registrasi = Column(Time)
    jam_mulai = Column(Time)
    jam_selesai = Column(Time)

    status = Column(String(50))
    keluhan = Column(String(255))