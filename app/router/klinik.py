from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.klinik import Klinik
from app.schemas.klinik import KlinikCreate, KlinikUpdate

router = APIRouter(prefix="/klinik", tags=["Klinik"])


@router.get("/")
def get_klinik(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    klinik = db.query(Klinik).first()
    if not klinik:
        raise HTTPException(status_code=404, detail="Profil klinik belum diisi")
    return klinik


@router.post("/")
def create_klinik(
    data: KlinikCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Klinik).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profil klinik sudah ada, gunakan PUT untuk update")

    klinik = Klinik(
        nama=data.nama,
        alamat=data.alamat,
        telepon=data.telepon,
        logo=data.logo,
    )
    db.add(klinik)
    db.commit()
    db.refresh(klinik)
    return klinik


@router.put("/{id_klinik}")
def update_klinik(
    id_klinik: int,
    data: KlinikUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    klinik = db.query(Klinik).filter(Klinik.id_klinik == id_klinik).first()
    if not klinik:
        raise HTTPException(status_code=404, detail="Profil klinik tidak ditemukan")

    if data.nama is not None:
        klinik.nama = data.nama
    if data.alamat is not None:
        klinik.alamat = data.alamat
    if data.telepon is not None:
        klinik.telepon = data.telepon
    if data.logo is not None:
        klinik.logo = data.logo

    db.commit()
    db.refresh(klinik)
    return klinik
