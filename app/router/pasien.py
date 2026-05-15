from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.pasien import Pasien

router = APIRouter(prefix="/pasien", tags=["Pasien"])


@router.get("/search")
def search_pasien(
    nama: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Pasien)
        .filter(Pasien.nama.ilike(f"%{nama}%"))
        .order_by(Pasien.nama.asc())
        .all()
    )
