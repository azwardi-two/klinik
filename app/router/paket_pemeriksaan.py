from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.paket_pemeriksaan_service import PaketPemeriksaanService
from app.schemas.paket_pemeriksaan import PaketPemeriksaanCreate, PaketPemeriksaanUpdate

router = APIRouter(prefix="/paket-pemeriksaan", tags=["Paket Pemeriksaan"])


@router.get("/")
def list_paket(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaketPemeriksaanService(db)
    return service.get_all_paket()


@router.get("/{id_paket}")
def get_paket(
    id_paket: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaketPemeriksaanService(db)
    result = service.get_paket(id_paket)
    if not result:
        raise HTTPException(status_code=404, detail="Paket tidak ditemukan")
    return result


@router.post("/")
def create_paket(
    data: PaketPemeriksaanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaketPemeriksaanService(db)
    return service.create_paket(data)


@router.put("/{id_paket}")
def update_paket(
    id_paket: int,
    data: PaketPemeriksaanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaketPemeriksaanService(db)
    result = service.update_paket(id_paket, data)
    if not result:
        raise HTTPException(status_code=404, detail="Paket tidak ditemukan")
    return result


@router.delete("/{id_paket}")
def delete_paket(
    id_paket: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaketPemeriksaanService(db)
    if not service.delete_paket(id_paket):
        raise HTTPException(status_code=404, detail="Paket tidak ditemukan")
    return {"message": "Paket berhasil dihapus"}
