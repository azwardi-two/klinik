from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.barang_service import BarangService
from app.schemas.barang import BarangCreate, BarangUpdate, PenerimaanRequest, PemakaianRequest

router = APIRouter(prefix="/barang", tags=["Barang / Inventory"])


@router.get("/")
def list_barang(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    return service.get_barang_with_stok_all()


@router.get("/{id_barang}")
def get_barang(
    id_barang: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    result = service.get_barang(id_barang)
    if not result:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return result


@router.post("/")
def create_barang(
    data: BarangCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    return service.create_barang(data)


@router.put("/{id_barang}")
def update_barang(
    id_barang: int,
    data: BarangUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    result = service.update_barang(id_barang, data)
    if not result:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return result


@router.delete("/{id_barang}")
def delete_barang(
    id_barang: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    if not service.delete_barang(id_barang):
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return {"message": "Barang berhasil dihapus"}


@router.post("/{id_barang}/masuk")
def barang_masuk(
    id_barang: int,
    data: PenerimaanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    result = service.barang_masuk(id_barang, data)
    if not result:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return result


@router.post("/{id_barang}/keluar")
def barang_keluar(
    id_barang: int,
    data: PemakaianRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    result = service.barang_keluar(id_barang, data)
    if not result:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return result


@router.get("/{id_barang}/mutasi")
def mutasi_barang(
    id_barang: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BarangService(db)
    result = service.get_mutasi(id_barang)
    if not result:
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    return result
