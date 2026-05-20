from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BarangCreate(BaseModel):
    id_jenis_tabung: Optional[int] = None
    nama_barang: str
    kategori: Optional[str] = "BAHAN_PAKAI"
    satuan: Optional[str] = None
    harga_satuan: Optional[int] = 0
    stok_minimum: Optional[int] = 0


class BarangUpdate(BaseModel):
    id_jenis_tabung: Optional[int] = None
    nama_barang: Optional[str] = None
    kategori: Optional[str] = None
    satuan: Optional[str] = None
    harga_satuan: Optional[int] = None
    stok_minimum: Optional[int] = None


class BarangResponse(BaseModel):
    id_barang: int
    id_jenis_tabung: Optional[int] = None
    nama_barang: str
    kategori: Optional[str] = None
    satuan: Optional[str] = None
    harga_satuan: int
    stok_minimum: int

    model_config = {"from_attributes": True}


class BarangStokResponse(BarangResponse):
    stok: int = 0


class PenerimaanRequest(BaseModel):
    jumlah: int
    harga_satuan: Optional[int] = None


class PemakaianRequest(BaseModel):
    id_tabung: Optional[int] = None
    jumlah_pakai: int


class MutasiResponse(BaseModel):
    id: int
    id_barang: int
    tipe: str
    jumlah: int
    harga_satuan: Optional[int] = None
    created_at: Optional[datetime] = None
