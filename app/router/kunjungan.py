from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.kunjungan_service import KunjunganService
from app.schemas.kunjungan import KunjunganCreate

router = APIRouter(prefix="/kunjungan")


@router.post("/")
def create_kunjungan(data: KunjunganCreate, db: Session = Depends(get_db)):
    service = KunjunganService(db)
    return service.create_kunjungan(data)


@router.get("/")
def list_kunjungan(
    tgl_awal: date = Query(...),
    tgl_akhir: date = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = KunjunganService(db)
    return service.get_all_kunjungan(tgl_awal, tgl_akhir, page, limit)