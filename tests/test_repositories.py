import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.repositories.publisher_repository import PublisherRepository


TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_publisher_repository():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию и репозиторий
    db = TestingSessionLocal()
    repo = PublisherRepository(db)
    
    # Тестируем создание
    publisher_data = {"name": "Test Publisher", "city": "Test City"}
    publisher = repo.create(publisher_data)
    
    assert publisher.id is not None
    assert publisher.name == "Test Publisher"
    
    # Тестируем получение
    publisher_from_db = repo.get_by_id(publisher.id)
    assert publisher_from_db.name == "Test Publisher"
    
    # Очистка
    db.close()