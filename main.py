from fastapi import FastAPI
#from app.api import pasien
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Klinik")

#app.include_router(pasien.router)