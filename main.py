from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.router import kunjungan, pasien, auth, pemeriksaan, paket_pemeriksaan, nilai_normal, pemeriksaan_pasien, hasil_pemeriksaan, tagihan, dashboard
from app.models import user as user_model
from app.models import pemeriksaan as pemeriksaan_model
from app.models import paket_pemeriksaan as paket_pemeriksaan_model
from app.models import nilai_normal as nilai_normal_model
from app.models import pemeriksaan_lab as pemeriksaan_lab_model
from app.models import pemeriksaan_pasien as pemeriksaan_pasien_model
from app.models import hasil_pemeriksaan as hasil_pemeriksaan_model
from app.models import tagihan as tagihan_model
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Klinik")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pasien.router)
app.include_router(kunjungan.router)
app.include_router(auth.router)
app.include_router(pemeriksaan.router)
app.include_router(paket_pemeriksaan.router)
app.include_router(nilai_normal.router)
app.include_router(pemeriksaan_pasien.router)
app.include_router(pemeriksaan_pasien.router_mulai)
app.include_router(hasil_pemeriksaan.router)
app.include_router(tagihan.router)
app.include_router(tagihan.router_tagihan)
app.include_router(dashboard.router)

app.mount("/", StaticFiles(directory="front_end", html=True), name="frontend")
