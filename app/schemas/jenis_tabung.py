from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class JenisTabungCreate(BaseModel):
    nama_jenis_tabung: str
    warna: Optional[str] = None
    volume_ml: Optional[float] = None
    keterangan: Optional[str] = None


class JenisTabungUpdate(BaseModel):
    nama_jenis_tabung: Optional[str] = None
    warna: Optional[str] = None
    volume_ml: Optional[float] = None
    keterangan: Optional[str] = None


class JenisTabungResponse(BaseModel):
    id_jenis_tabung: int
    nama_jenis_tabung: str
    warna: Optional[str] = None
    volume_ml: Optional[float] = None
    keterangan: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
