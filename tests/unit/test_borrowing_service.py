import pytest
from datetime import date
from unittest.mock import Mock, MagicMock
from app.services.borrowing_service import BorrowingService
from app.schemas.borrowing import BorrowingCreate
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrowing import Borrowing

def test_create_borrowing_success():
    # Мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    # Настраиваем моки
    mock_reader = Mock(spec=Reader)
    mock_reader.id = 1
    mock_reader_repo.get_by_id.return_value = mock_reader
    
    mock_book = Mock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.quantity = 5
    mock_book_repo.get_by_id.return_value = mock_book
    
    mock_borrowing_repo.get_reader_active_borrowings_count.return_value = 3
    
    mock_borrowing = Mock(spec=Borrowing)
    mock_borrowing.id = 1
    mock_borrowing.reader_id = 1
    mock_borrowing.book_id = 1
    mock_borrowing_repo.create.return_value = mock_borrowing
    
    mock_updated_book = Mock(spec=Book)
    mock_book_repo.decrease_quantity.return_value = mock_updated_book
    
    # Создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # Вызываем метод
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    result = service.create_borrowing(borrowing_data)
    
    # Проверяем
    assert result is not None
    mock_book_repo.decrease_quantity.assert_called_once_with(1, 1)
    mock_borrowing_repo.create.assert_called_once()

def test_create_borrowing_no_reader():
    # Мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    # Настраиваем моки (читатель не найден)
    mock_reader_repo.get_by_id.return_value = None
    
    # Создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # Вызываем метод и ожидаем ошибку
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    
    with pytest.raises(ValueError, match="Reader not found"):
        service.create_borrowing(borrowing_data)

def test_create_borrowing_book_unavailable():
    # Мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    # Настраиваем моки (книга недоступна)
    mock_reader = Mock(spec=Reader)
    mock_reader.id = 1
    mock_reader_repo.get_by_id.return_value = mock_reader
    
    mock_book = Mock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.quantity = 0  # Нет доступных книг
    mock_book_repo.get_by_id.return_value = mock_book
    
    # Создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # Вызываем метод и ожидаем ошибку
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    
    with pytest.raises(ValueError, match="Book is not available"):
        service.create_borrowing(borrowing_data)

def test_create_borrowing_too_many_books():
    # Мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    # Настраиваем моки (читатель уже имеет 5 книг)
    mock_reader = Mock(spec=Reader)
    mock_reader.id = 1
    mock_reader_repo.get_by_id.return_value = mock_reader
    
    mock_book = Mock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.quantity = 5
    mock_book_repo.get_by_id.return_value = mock_book
    
    mock_borrowing_repo.get_reader_active_borrowings_count.return_value = 5  # Уже 5 книг
    
    # Создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # Вызываем метод и ожидаем ошибку
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    
    with pytest.raises(ValueError, match="Reader cannot borrow more than 5 books"):
        service.create_borrowing(borrowing_data)