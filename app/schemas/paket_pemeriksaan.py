from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class PaketPemeriksaanDetailItem(BaseModel):
    id_pemeriksaan: int


class PaketPemeriksaanCreate(BaseModel):
    nama_paket: str
    biaya_paket: Optional[int] = 0
    keterangan: Optional[str] = None
    detail_items: Optional[List[PaketPemeriksaanDetailItem]] = None


class PaketPemeriksaanUpdate(BaseModel):
    nama_paket: Optional[str] = None
    biaya_paket: Optional[int] = None
    keterangan: Optional[str] = None
    detail_items: Optional[List[PaketPemeriksaanDetailItem]] = None


class PaketPemeriksaanDetailResponse(BaseModel):
    id: int
    id_paket: int
    id_pemeriksaan: int

    model_config = {"from_attributes": True}


class PaketPemeriksaanResponse(BaseModel):
    id_paket: int
    nama_paket: str
    biaya_paket: int
    keterangan: Optional[str] = None
    created_at: Optional[datetime] = None
    detail_items: Optional[List[PaketPemeriksaanDetailResponse]] = None

    model_config = {"from_attributes": True}
