from typing import Optional

from pydantic import BaseModel
from datetime import date

class KunjunganCreate(BaseModel):
    idpasien:  Optional[int] = None
    keluhan: str
    tgl_kunjungan: date
   