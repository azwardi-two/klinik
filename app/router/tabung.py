from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.tabung_service import TabungService
from app.services.barang_service import BarangService

router = APIRouter(prefix="/tabung", tags=["Tabung"])


@router.get("/")
def list_tabung(
    id_lab: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TabungService(db)
    if id_lab:
        return service.get_by_lab(id_lab)
    return service.get_all()


@router.get("/barcode/{barcode}")
def get_tabung_by_barcode(
    barcode: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TabungService(db)
    result = service.scan_barcode(barcode)
    if not result:
        raise HTTPException(status_code=404, detail="Tabung tidak ditemukan")
    return result


@router.put("/{id_tabung}/ambil")
def ambil_sampel(
    id_tabung: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TabungService(db)
    result = service.ambil_sampel(id_tabung)
    if not result:
        raise HTTPException(status_code=404, detail="Tabung tidak ditemukan")
    return result
