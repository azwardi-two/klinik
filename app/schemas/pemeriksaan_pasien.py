from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class PemeriksaanPasienItem(BaseModel):
    jenis: str
    id_pemeriksaan: Optional[int] = None
    id_paket: Optional[int] = None


class PemeriksaanPasienCreate(BaseModel):
    items: List[PemeriksaanPasienItem]


class PemeriksaanPasienResponse(BaseModel):
    id: int
    id_pemeriksaan_lab: Optional[int] = None
    id_kunjungan: int
    jenis: str
    id_pemeriksaan: Optional[int] = None
    id_paket: Optional[int] = None
    biaya_dibebankan: int
    jam_mulai: Optional[datetime] = None
    jam_selesai: Optional[datetime] = None
    jam_seharusnya_selesai: Optional[datetime] = None
    status: str
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
