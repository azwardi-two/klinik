from pydantic import BaseModel
from datetime import date

class KunjunganCreate(BaseModel):
    idpasien: int
    tanggal_kunjungan: date
    keluhan: str