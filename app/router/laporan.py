from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.laporan_service import generate_lab_pdf, generate_tagihan_pdf

router = APIRouter(tags=["Laporan"])


@router.get("/kunjungan/{id_kunjungan}/cetak-lab")
def cetak_lab_pdf(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        pdf_bytes = generate_lab_pdf(db, id_kunjungan)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=hasil_lab_{id_kunjungan}.pdf"
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal generate PDF: {str(e)}")


@router.get("/kunjungan/{id_kunjungan}/cetak-tagihan")
def cetak_tagihan_pdf(
    id_kunjungan: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        pdf_bytes = generate_tagihan_pdf(db, id_kunjungan)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=tagihan_{id_kunjungan}.pdf"
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal generate PDF tagihan: {str(e)}")
