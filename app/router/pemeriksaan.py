from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.pemeriksaan_service import PemeriksaanService
from app.schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate

router = APIRouter(prefix="/pemeriksaan", tags=["Pemeriksaan"])


@router.get("/")
def list_pemeriksaan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanService(db)
    return service.get_all_pemeriksaan()


@router.get("/{id_pemeriksaan}")
def get_pemeriksaan(
    id_pemeriksaan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanService(db)
    result = service.get_pemeriksaan(id_pemeriksaan)
    if not result:
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")
    return result


@router.post("/")
def create_pemeriksaan(
    data: PemeriksaanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanService(db)
    return service.create_pemeriksaan(data)


@router.put("/{id_pemeriksaan}")
def update_pemeriksaan(
    id_pemeriksaan: int,
    data: PemeriksaanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanService(db)
    result = service.update_pemeriksaan(id_pemeriksaan, data)
    if not result:
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")
    return result


@router.delete("/{id_pemeriksaan}")
def delete_pemeriksaan(
    id_pemeriksaan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PemeriksaanService(db)
    if not service.delete_pemeriksaan(id_pemeriksaan):
        raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")
    return {"message": "Pemeriksaan berhasil dihapus"}
