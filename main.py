from fastapi import FastAPI
#from app.api import pasien
from app.core.database import Base, engine
from app.router import kunjungan
from fastapi.middleware.cors import CORSMiddleware

from app.router import pasien


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Klinik")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk dev bebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pasien.router)
app.include_router(kunjungan.router)