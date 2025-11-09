import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, engine, Base

from app.models.publisher import Publisher
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrowing import Borrowing

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_publishers():
    db = SessionLocal()
    try:
        publisher = Publisher(name="Test Publisher", city="Test City")
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
        
        response = client.get("/publishers/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    finally:
        # Очищаем тестовые данные
        db.query(Publisher).delete()
        db.commit()
        db.close()

def test_create_publisher():
    publisher_data = {
        "name": "New Test Publisher",
        "city": "New Test City"
    }
    response = client.post("/publishers/", json=publisher_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == publisher_data["name"]
    assert data["city"] == publisher_data["city"]
    assert "id" in data
    
    # Очищаем
    db = SessionLocal()
    db.query(Publisher).filter(Publisher.name == "New Test Publisher").delete()
    db.commit()
    db.close()