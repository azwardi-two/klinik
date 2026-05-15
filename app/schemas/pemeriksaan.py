from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PemeriksaanCreate(BaseModel):
    nama_pemeriksaan: str
    biaya: Optional[int] = 0
    lama_waktu: Optional[int] = 0
    kategori: Optional[str] = None


class PemeriksaanUpdate(BaseModel):
    nama_pemeriksaan: Optional[str] = None
    biaya: Optional[int] = None
    lama_waktu: Optional[int] = None
    kategori: Optional[str] = None


class PemeriksaanResponse(BaseModel):
    id_pemeriksaan: int
    nama_pemeriksaan: str
    biaya: int
    lama_waktu: int
    kategori: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
