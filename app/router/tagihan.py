from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.tagihan_service import TagihanService

router = APIRouter(prefix="/kunjungan", tags=["Tagihan"])


@router.post("/{id_kunjungan}/tagihan")
def generate_tagihan(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TagihanService(db)
    try:
        return service.generate_tagihan(id_kunjungan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id_kunjungan}/tagihan")
def get_tagihan(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TagihanService(db)
    result = service.get_tagihan(id_kunjungan)
    if not result:
        raise HTTPException(status_code=404, detail="Tagihan tidak ditemukan")
    return result


router_tagihan = APIRouter(prefix="/tagihan", tags=["Tagihan"])


@router_tagihan.put("/{id_tagihan}/bayar")
def bayar_tagihan(
    id_tagihan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TagihanService(db)
    try:
        result = service.bayar_tagihan(id_tagihan)
        if not result:
            raise HTTPException(status_code=404, detail="Tagihan tidak ditemukan")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
