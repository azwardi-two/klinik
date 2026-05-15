from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.kunjungan_service import KunjunganService
from app.schemas.kunjungan import KunjunganCreate

router = APIRouter(prefix="/kunjungan", tags=["Kunjungan"])


@router.post("/")
def create_kunjungan(
    data: KunjunganCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = KunjunganService(db)
    return service.create_kunjungan(data, current_user)


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
