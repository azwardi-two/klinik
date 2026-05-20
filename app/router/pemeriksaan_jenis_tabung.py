from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.pemeriksaan_jenis_tabung import PemeriksaanJenisTabung
from app.models.pemeriksaan import Pemeriksaan
from app.models.jenis_tabung import JenisTabung
from app.schemas.pemeriksaan_jenis_tabung import PemeriksaanJenisTabungCreate
from app.repositories.pemeriksaan_jenis_tabung import PemeriksaanJenisTabungRepository
from app.core.uow import UnitOfWork

router = APIRouter(prefix="/pemeriksaan-jenis-tabung", tags=["Mapping Pemeriksaan ke Tabung"])


@router.get("/")
def list_mapping(
    id_pemeriksaan: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = PemeriksaanJenisTabungRepository(db)
    if id_pemeriksaan:
        rows = repo.get_by_pemeriksaan(id_pemeriksaan)
    else:
        rows = repo.get_all()
    result = []
    for r in rows:
        px = db.query(Pemeriksaan).get(r.id_pemeriksaan)
        jt = db.query(JenisTabung).get(r.id_jenis_tabung)
        result.append({
            "id": r.id,
            "id_pemeriksaan": r.id_pemeriksaan,
            "id_jenis_tabung": r.id_jenis_tabung,
            "jumlah_tabung": r.jumlah_tabung,
            "nama_pemeriksaan": px.nama_pemeriksaan if px else None,
            "nama_jenis_tabung": jt.nama_jenis_tabung if jt else None,
            "warna": jt.warna if jt else None,
        })
    return result


@router.post("/")
def create_mapping(
    data: PemeriksaanJenisTabungCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    with UnitOfWork(db) as uow:
        existing = db.query(PemeriksaanJenisTabung).filter(
            PemeriksaanJenisTabung.id_pemeriksaan == data.id_pemeriksaan,
            PemeriksaanJenisTabung.id_jenis_tabung == data.id_jenis_tabung,
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Mapping sudah ada")
        r = PemeriksaanJenisTabung(
            id_pemeriksaan=data.id_pemeriksaan,
            id_jenis_tabung=data.id_jenis_tabung,
            jumlah_tabung=data.jumlah_tabung or 1,
        )
        db.add(r)
        uow.flush()
        return {
            "id": r.id,
            "id_pemeriksaan": r.id_pemeriksaan,
            "id_jenis_tabung": r.id_jenis_tabung,
            "jumlah_tabung": r.jumlah_tabung,
        }


@router.delete("/{id}")
def delete_mapping(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    with UnitOfWork(db) as uow:
        repo = PemeriksaanJenisTabungRepository(db)
        r = repo.get_by_id(id)
        if not r:
            raise HTTPException(status_code=404, detail="Mapping tidak ditemukan")
        repo.delete(r)
        return {"message": "Mapping berhasil dihapus"}
