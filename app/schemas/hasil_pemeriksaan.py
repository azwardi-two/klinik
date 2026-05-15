from typing import Optional
from pydantic import BaseModel


class HasilPemeriksaanUpdate(BaseModel):
    nilai_bawah: Optional[float] = None
    nilai_atas: Optional[float] = None
    nilai_value: Optional[float] = None
    nilai_text: Optional[str] = None
    keterangan: Optional[str] = None


class HasilPemeriksaanResponse(BaseModel):
    id: int
    id_pemeriksaan_pasien: int
    id_pemeriksaan: int
    nilai_bawah: Optional[float] = None
    nilai_atas: Optional[float] = None
    nilai_value: Optional[float] = None
    nilai_text: Optional[str] = None
    status_nilai: Optional[str] = None
    keterangan: Optional[str] = None

    model_config = {"from_attributes": True}
