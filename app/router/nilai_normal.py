from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.nilai_normal_service import NilaiNormalService
from app.schemas.nilai_normal import NilaiNormalCreate, NilaiNormalUpdate

router = APIRouter(prefix="/nilai-normal", tags=["Nilai Normal"])


@router.get("/")
def list_nilai_normal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    return service.get_all_nilai_normal()


@router.get("/{id_nilai_normal}")
def get_nilai_normal(
    id_nilai_normal: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    result = service.get_nilai_normal(id_nilai_normal)
    if not result:
        raise HTTPException(status_code=404, detail="Nilai normal tidak ditemukan")
    return result


@router.get("/pemeriksaan/{id_pemeriksaan}")
def get_nilai_normal_by_pemeriksaan(
    id_pemeriksaan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    return service.get_by_pemeriksaan(id_pemeriksaan)


@router.post("/")
def create_nilai_normal(
    data: NilaiNormalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    return service.create_nilai_normal(data)


@router.put("/{id_nilai_normal}")
def update_nilai_normal(
    id_nilai_normal: int,
    data: NilaiNormalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    result = service.update_nilai_normal(id_nilai_normal, data)
    if not result:
        raise HTTPException(status_code=404, detail="Nilai normal tidak ditemukan")
    return result


@router.delete("/{id_nilai_normal}")
def delete_nilai_normal(
    id_nilai_normal: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NilaiNormalService(db)
    if not service.delete_nilai_normal(id_nilai_normal):
        raise HTTPException(status_code=404, detail="Nilai normal tidak ditemukan")
    return {"message": "Nilai normal berhasil dihapus"}
