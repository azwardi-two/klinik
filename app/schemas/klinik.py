from pydantic import BaseModel
from typing import Optional


class KlinikCreate(BaseModel):
    nama: str
    alamat: Optional[str] = None
    telepon: Optional[str] = None
    logo: Optional[str] = None


class KlinikUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    telepon: Optional[str] = None
    logo: Optional[str] = None


class KlinikResponse(BaseModel):
    id_klinik: int
    nama: str
    alamat: Optional[str] = None
    telepon: Optional[str] = None
    logo: Optional[str] = None

    class Config:
        from_attributes = True
