from tokenize import String
from typing import Optional

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