from fastapi import FastAPI
from app.core.database import Base, engine
from app.router import kunjungan, pasien, auth
from app.models import user as user_model
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Klinik")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pasien.router)
app.include_router(kunjungan.router)
app.include_router(auth.router)