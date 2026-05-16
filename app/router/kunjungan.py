from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.kunjungan_service import KunjunganService
from app.schemas.kunjungan import KunjunganCreate, KunjunganUpdate

router = APIRouter(prefix="/kunjungan", tags=["Kunjungan"])



@router.post("/")
def create_kunjungan(
    data: KunjunganCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = KunjunganService(db)
    return service.create_kunjungan(data, current_user)
    return service.create_kunjungan(data)


@router.get("/")
def list_kunjungan(
    tgl_awal: date = Query(...),
    tgl_akhir: date = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = KunjunganService(db)
    return service.get_all_kunjungan(tgl_awal, tgl_akhir, page, limit)


@router.put("/{id_kunjungan}")
def update_kunjungan(
    id_kunjungan: int,
    data: KunjunganUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = KunjunganService(db)
    result = service.update_kunjungan(id_kunjungan, data)
    if not result:
        raise HTTPException(status_code=404, detail="Kunjungan tidak ditemukan")
    return result


@router.delete("/{id_kunjungan}")
def delete_kunjungan(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = KunjunganService(db)
    if not service.delete_kunjungan(id_kunjungan):
        raise HTTPException(status_code=404, detail="Kunjungan tidak ditemukan")
    return {"message": "Kunjungan berhasil dihapus"}
