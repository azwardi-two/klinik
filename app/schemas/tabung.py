from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TabungResponse(BaseModel):
    id_tabung: int
    id_pemeriksaan_lab: int
    id_jenis_tabung: int
    barcode: str
    waktu_ambil: Optional[datetime] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TabungDetailResponse(TabungResponse):
    nama_jenis_tabung: Optional[str] = None
    warna: Optional[str] = None
    id_kunjungan: Optional[int] = None
    no_reg_kunjungan: Optional[str] = None
    nama_pasien: Optional[str] = None
