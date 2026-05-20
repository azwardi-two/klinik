from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Barang(Base):
    __tablename__ = "barang"

    id_barang = Column(Integer, primary_key=True)
    id_jenis_tabung = Column(Integer, ForeignKey("jenis_tabung.id_jenis_tabung"), nullable=True)
    nama_barang = Column(String(200), nullable=False)
    kategori = Column(String(20), default="BAHAN_PAKAI")
    satuan = Column(String(50))
    harga_satuan = Column(Integer, default=0)
    stok_minimum = Column(Integer, default=0)


class PenerimaanBarang(Base):
    __tablename__ = "penerimaan_barang"

    id = Column(Integer, primary_key=True)
    id_barang = Column(Integer, ForeignKey("barang.id_barang"), nullable=False)
    jumlah = Column(Integer, default=0)
    harga_satuan = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class PemakaianBarang(Base):
    __tablename__ = "pemakaian_barang"

    id = Column(Integer, primary_key=True)
    id_tabung = Column(Integer, ForeignKey("tabung.id_tabung"), nullable=True)
    id_barang = Column(Integer, ForeignKey("barang.id_barang"), nullable=False)
    jumlah_pakai = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
