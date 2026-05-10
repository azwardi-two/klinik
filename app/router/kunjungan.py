from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.kunjungan_service import KunjunganService
from app.schemas.kunjungan import KunjunganCreate

router = APIRouter(prefix="/kunjungan")

@router.post("/")
def create_kunjungan(data: KunjunganCreate, db: Session = Depends(get_db)):
    service = KunjunganService(db)
    return service.create_kunjungan(data)