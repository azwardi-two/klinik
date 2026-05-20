from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.jenis_tabung import JenisTabung
from app.schemas.jenis_tabung import JenisTabungCreate, JenisTabungUpdate
from app.core.uow import UnitOfWork

router = APIRouter(prefix="/jenis-tabung", tags=["Jenis Tabung"])


@router.get("/")
def list_jenis_tabung(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = db.query(JenisTabung).order_by(JenisTabung.nama_jenis_tabung.asc()).all()
    return [
        {
            "id_jenis_tabung": r.id_jenis_tabung,
            "nama_jenis_tabung": r.nama_jenis_tabung,
            "warna": r.warna,
            "volume_ml": r.volume_ml,
            "keterangan": r.keterangan,
            "created_at": str(r.created_at) if r.created_at else None,
        }
        for r in rows
    ]


@router.get("/{id_jenis_tabung}")
def get_jenis_tabung(
    id_jenis_tabung: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = db.query(JenisTabung).get(id_jenis_tabung)
    if not r:
        raise HTTPException(status_code=404, detail="Jenis tabung tidak ditemukan")
    return {
        "id_jenis_tabung": r.id_jenis_tabung,
        "nama_jenis_tabung": r.nama_jenis_tabung,
        "warna": r.warna,
        "volume_ml": r.volume_ml,
        "keterangan": r.keterangan,
        "created_at": str(r.created_at) if r.created_at else None,
    }


@router.post("/")
def create_jenis_tabung(
    data: JenisTabungCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    with UnitOfWork(db) as uow:
        r = JenisTabung(
            nama_jenis_tabung=data.nama_jenis_tabung,
            warna=data.warna,
            volume_ml=data.volume_ml,
            keterangan=data.keterangan,
        )
        db.add(r)
        uow.flush()
        return {
            "id_jenis_tabung": r.id_jenis_tabung,
            "nama_jenis_tabung": r.nama_jenis_tabung,
            "warna": r.warna,
            "volume_ml": r.volume_ml,
            "keterangan": r.keterangan,
        }


@router.put("/{id_jenis_tabung}")
def update_jenis_tabung(
    id_jenis_tabung: int,
    data: JenisTabungUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    with UnitOfWork(db) as uow:
        r = db.query(JenisTabung).get(id_jenis_tabung)
        if not r:
            raise HTTPException(status_code=404, detail="Jenis tabung tidak ditemukan")
        if data.nama_jenis_tabung is not None:
            r.nama_jenis_tabung = data.nama_jenis_tabung
        if data.warna is not None:
            r.warna = data.warna
        if data.volume_ml is not None:
            r.volume_ml = data.volume_ml
        if data.keterangan is not None:
            r.keterangan = data.keterangan
        return {
            "id_jenis_tabung": r.id_jenis_tabung,
            "nama_jenis_tabung": r.nama_jenis_tabung,
            "warna": r.warna,
            "volume_ml": r.volume_ml,
            "keterangan": r.keterangan,
        }


@router.delete("/{id_jenis_tabung}")
def delete_jenis_tabung(
    id_jenis_tabung: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    with UnitOfWork(db) as uow:
        r = db.query(JenisTabung).get(id_jenis_tabung)
        if not r:
            raise HTTPException(status_code=404, detail="Jenis tabung tidak ditemukan")
        db.delete(r)
        return {"message": "Jenis tabung berhasil dihapus"}
