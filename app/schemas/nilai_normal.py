from typing import Optional
from pydantic import BaseModel


class NilaiNormalCreate(BaseModel):
    id_pemeriksaan: int
    jenis_kelamin: Optional[str] = None
    usia_hari_min: Optional[int] = 0
    usia_hari_max: Optional[int] = 99999
    nilai_bawah: Optional[float] = None
    nilai_atas: Optional[float] = None
    operator: Optional[str] = None
    nilai_operator: Optional[float] = None
    nilai_text: Optional[str] = None
    keterangan: Optional[str] = None


class NilaiNormalUpdate(BaseModel):
    jenis_kelamin: Optional[str] = None
    usia_hari_min: Optional[int] = None
    usia_hari_max: Optional[int] = None
    nilai_bawah: Optional[float] = None
    nilai_atas: Optional[float] = None
    operator: Optional[str] = None
    nilai_operator: Optional[float] = None
    nilai_text: Optional[str] = None
    keterangan: Optional[str] = None


class NilaiNormalResponse(BaseModel):
    id_nilai_normal: int
    id_pemeriksaan: int
    jenis_kelamin: Optional[str] = None
    usia_hari_min: int
    usia_hari_max: int
    nilai_bawah: Optional[float] = None
    nilai_atas: Optional[float] = None
    operator: Optional[str] = None
    nilai_operator: Optional[float] = None
    nilai_text: Optional[str] = None
    keterangan: Optional[str] = None

    model_config = {"from_attributes": True}
