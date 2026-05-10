from pydantic import BaseModel
from datetime import date

class PasienCreate(BaseModel):
    nama: str
    alamat: str
    jenis_kelamin: str
    tgl_lahir: date
    no_hp: str