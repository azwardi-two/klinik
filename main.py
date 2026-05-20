from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.router import kunjungan, pasien, auth, pemeriksaan, paket_pemeriksaan, nilai_normal, pemeriksaan_pasien, hasil_pemeriksaan, tagihan, dashboard, klinik, laporan, jenis_tabung, tabung as tabung_router, barang, pemeriksaan_jenis_tabung
from app.models import user as user_model
from app.models import pemeriksaan as pemeriksaan_model
from app.models import paket_pemeriksaan as paket_pemeriksaan_model
from app.models import nilai_normal as nilai_normal_model
from app.models import pemeriksaan_lab as pemeriksaan_lab_model
from app.models import pemeriksaan_pasien as pemeriksaan_pasien_model
from app.models import hasil_pemeriksaan as hasil_pemeriksaan_model
from app.models import tagihan as tagihan_model
from app.models import klinik as klinik_model
from app.models import jenis_tabung as jenis_tabung_model
from app.models import tabung as tabung_model
from app.models import barang as barang_model
from app.models import pemeriksaan_jenis_tabung as pemeriksaan_jenis_tabung_model
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
app.include_router(klinik.router)
app.include_router(laporan.router)
app.include_router(jenis_tabung.router)
app.include_router(tabung_router.router)
app.include_router(barang.router)
app.include_router(pemeriksaan_jenis_tabung.router)

app.mount("/", StaticFiles(directory="front_end", html=True), name="frontend")
