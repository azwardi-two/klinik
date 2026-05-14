from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.pasien_service import PasienService
from app.models.pasien import Pasien #from app.schemas.kunjungan import KunjunganCreate

router = APIRouter(prefix="/pasien")

@router.get("/search")
def search_pasien(nama: str,db: Session = Depends(get_db)):
    return db.query(Pasien).filter(Pasien.nama.ilike(f"%{nama}%")).order_by(Pasien.nama.asc()).all()