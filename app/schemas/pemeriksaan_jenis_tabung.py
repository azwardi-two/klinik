from typing import Optional
from pydantic import BaseModel


class PemeriksaanJenisTabungCreate(BaseModel):
    id_pemeriksaan: int
    id_jenis_tabung: int
    jumlah_tabung: Optional[int] = 1


class PemeriksaanJenisTabungResponse(BaseModel):
    id: int
    id_pemeriksaan: int
    id_jenis_tabung: int
    jumlah_tabung: int

    model_config = {"from_attributes": True}


class PemeriksaanJenisTabungDetailResponse(PemeriksaanJenisTabungResponse):
    nama_pemeriksaan: Optional[str] = None
    nama_jenis_tabung: Optional[str] = None
    warna: Optional[str] = None
