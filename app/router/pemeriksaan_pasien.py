from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.pemeriksaan_pasien_service import PemeriksaanPasienService
from app.schemas.pemeriksaan_pasien import PemeriksaanPasienCreate

router = APIRouter(prefix="/kunjungan", tags=["Pemeriksaan Pasien"])


@router.post("/{id_kunjungan}/pemeriksaan")
def add_pemeriksaan(
    id_kunjungan: int,
    data: PemeriksaanPasienCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    try:
        return service.add_pemeriksaan(id_kunjungan, data, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id_kunjungan}/pemeriksaan")
def list_pemeriksaan(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    return service.list_pemeriksaan(id_kunjungan)


@router.put("/{id_kunjungan}/pemeriksaan-lab/mulai")
def mulai_pemeriksaan_lab(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    try:
        result = service.mulai_pemeriksaan_lab(id_kunjungan, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Kunjungan tidak ditemukan")
    return result


@router.put("/{id_kunjungan}/pemeriksaan-lab/selesai")
def selesai_pemeriksaan_lab(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    try:
        result = service.selesai_pemeriksaan_lab(id_kunjungan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Pemeriksaan lab tidak ditemukan")
    return result


router_mulai = APIRouter(prefix="/pemeriksaan-pasien", tags=["Pemeriksaan Pasien"])


@router_mulai.put("/{id}/mulai")
def mulai_pemeriksaan(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    try:
        result = service.mulai_pemeriksaan(id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Pemeriksaan pasien tidak ditemukan")
    return result


@router_mulai.put("/{id}/selesai")
def selesai_pemeriksaan(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanPasienService(db)
    result = service.selesai_pemeriksaan(id)
    if not result:
        raise HTTPException(status_code=404, detail="Pemeriksaan pasien tidak ditemukan")
    return result
