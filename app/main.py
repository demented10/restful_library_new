from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.config import settings

Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Library API", version = "v1")

@app.get("/")
def read_root():
    return {"message": "Hello its library api"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}