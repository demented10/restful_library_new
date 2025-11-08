from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.core.database import engine, Base, get_db
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    Base.metadata.create_all(bind = engine)
    logger.info("db tables created succesfully")
except Exception as e:
    logger.error(f"db tables creation error : {e}")

app = FastAPI(title = "Library API", version = "v1")

@app.get("/")
def read_root():
    return {"message": "Hello its library api"}

@app.get("/health")
def health_check(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"db health status check failed: {e}")
        return {"status": "unhealthy", "database": "disconected"}