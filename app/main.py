from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.config import settings

from app.models import publisher, book, reader, borrowing


from app.api.routes import publishers, books, readers, borrowings, reports

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title="Library API", 
    version="1.0.0",
    description="API для управления библиотекой с системой учета книг и читателей"
)
app.include_router(publishers.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrowings.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Library API"}

@app.get("/health")
def health_check():
    return {"statusss": "healthy", "database": "connected"}

