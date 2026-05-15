from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class TagihanDetailResponse(BaseModel):
    id: int
    id_pemeriksaan_pasien: int
    biaya: int

    model_config = {"from_attributes": True}


class TagihanResponse(BaseModel):
    id: int
    id_kunjungan: int
    tgl_tagihan: Optional[datetime] = None
    total_biaya: int
    status_tagihan: str
    details: Optional[List[TagihanDetailResponse]] = None

    model_config = {"from_attributes": True}
