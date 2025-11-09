import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.repositories.publisher_repository import PublisherRepository
from app.repositories.book_repository import BookRepository
from app.repositories.reader_repository import ReaderRepository
from app.repositories.borrowing_repository import BorrowingRepository

from app.models.publisher import Publisher
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrowing import Borrowing

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module(module):
    """Создаем таблицы перед запуском тестов"""
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    """Очищаем после тестов"""
    Base.metadata.drop_all(bind=engine)

def test_publisher_repository():
    db = TestingSessionLocal()
    try:
        repo = PublisherRepository(db)
        
        # Тестируем создание
        publisher_data = {"name": "Test Publisher", "city": "Test City"}
        publisher = repo.create(publisher_data)
        
        assert publisher.id is not None
        assert publisher.name == "Test Publisher"
        
        # Тестируем получение
        publisher_from_db = repo.get_by_id(publisher.id)
        assert publisher_from_db.name == "Test Publisher"
        
        # Тестируем получение всех
        all_publishers = repo.get_all()
        assert len(all_publishers) == 1
        
        # Тестируем обновление
        updated_publisher = repo.update(publisher.id, {"city": "Updated City"})
        assert updated_publisher.city == "Updated City"
        
        # тестируем удаление
        result = repo.delete(publisher.id)
        assert result is True
        
        # Проверяем что удалилось
        deleted_publisher = repo.get_by_id(publisher.id)
        assert deleted_publisher is None
        
    finally:
        db.close()

def test_book_repository():
    db = TestingSessionLocal()
    try:
        # создаем издателя
        publisher_repo = PublisherRepository(db)
        publisher = publisher_repo.create({"name": "Book Test Publisher", "city": "Test City"})
        
        # Тестируем репозиторий книг
        book_repo = BookRepository(db)
        
        book_data = {
            "title": "Test Book",
            "author": "Test Author", 
            "year": 2023,
            "price": 500,
            "quantity": 10,
            "publisher_id": publisher.id
        }
        
        book = book_repo.create(book_data)
        assert book.id is not None
        assert book.title == "Test Book"
        
        # Тестируем поиск
        found_books = book_repo.search_books("Test")
        assert len(found_books) == 1
        
        # Тестируем обновление количества
        updated_book = book_repo.decrease_quantity(book.id, 2)
        assert updated_book.quantity == 8
        
    finally:
        db.close()

def test_reader_repository():
    db = TestingSessionLocal()
    try:
        repo = ReaderRepository(db)
        
        reader_data = {
            "full_name": "Test Reader",
            "address": "Test Address", 
            "phone": "+7-999-999-99-99"
        }
        
        reader = repo.create(reader_data)
        assert reader.id is not None
        assert reader.full_name == "Test Reader"
        
        # Тестируем поиск по телефону
        found_reader = repo.get_by_phone("+7-999-999-99-99")
        assert found_reader.id == reader.id
        
    finally:
        db.close()