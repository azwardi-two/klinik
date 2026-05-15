from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.hasil_pemeriksaan_service import HasilPemeriksaanService
from app.schemas.hasil_pemeriksaan import HasilPemeriksaanUpdate

router = APIRouter(prefix="/hasil-pemeriksaan", tags=["Hasil Pemeriksaan"])


@router.get("/{id_pemeriksaan_pasien}")
def get_hasil(
    id_pemeriksaan_pasien: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = HasilPemeriksaanService(db)
    return service.get_hasil_by_pemeriksaan_pasien(id_pemeriksaan_pasien)


@router.put("/{id}")
def update_hasil(
    id: int,
    data: HasilPemeriksaanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = HasilPemeriksaanService(db)
    result = service.update_hasil(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Hasil pemeriksaan tidak ditemukan")
    return result
