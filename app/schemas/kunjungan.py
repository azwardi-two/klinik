from typing import Optional, List

from pydantic import BaseModel
from datetime import date

class KunjunganCreate(BaseModel):
    idpasien:  Optional[int] = None
    keluhan: str
    tgl_kunjungan: date
    nama:  Optional[str] = None
    alamat  :  Optional[str] = None
    tgl_lahir: Optional[date] = None              
    jenis_kelamin: Optional[str] = None              
    no_hp: Optional[str] = None

class KunjunganUpdate(BaseModel):
    keluhan: Optional[str] = None
    tgl_kunjungan: Optional[date] = None
    status: Optional[str] = None

class KunjunganListItem(BaseModel):
    tgl_kunjungan: date
    no_reg: str
    nama_pasien: str
    keluhan: str
    status: str

class KunjunganListResponse(BaseModel):
    data: List[KunjunganListItem]
    total: int
    page: int
    limit: int
    total_pages: int
