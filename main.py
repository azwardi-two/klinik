from fastapi import FastAPI
#from app.api import pasien
from app.core.database import Base, engine
from app.router import kunjungan

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Klinik")

#app.include_router(pasien.router)
app.include_router(kunjungan.router)