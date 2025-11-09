import pytest
from datetime import date, timedelta
from unittest.mock import Mock
from app.services.borrowing_service import BorrowingService
from app.schemas.borrowing import BorrowingCreate

def test_create_borrowing_success():
    #мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    #настраиваем моки
    mock_reader_repo.get_by_id.return_value = Mock(id=1, full_name="Test Reader")
    mock_book_repo.get_by_id.return_value = Mock(id=1, title="Test Book", quantity=5)
    mock_borrowing_repo.get_reader_active_borrowings_count.return_value = 3
    mock_borrowing_repo.create.return_value = Mock(id=1, reader_id=1, book_id=1)
    
    #создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    #вызываем метод
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    result = service.create_borrowing(borrowing_data)
    
    #проверяем
    assert result is not None
    mock_book_repo.decrease_quantity.assert_called_once_with(1, 1)
    mock_borrowing_repo.create.assert_called_once()

def test_create_borrowing_no_reader():
    #мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    #настраиваем моки (читатель не найден)
    mock_reader_repo.get_by_id.return_value = None
    
    #создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # вызываем метод и ожидаем ошибку
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    
    with pytest.raises(ValueError, match="Reader not found"):
        service.create_borrowing(borrowing_data)

def test_create_borrowing_book_unavailable():
    # мокируем репозитории
    mock_borrowing_repo = Mock()
    mock_book_repo = Mock()
    mock_reader_repo = Mock()
    
    #настраиваем моки (книга недоступна)
    mock_reader_repo.get_by_id.return_value = Mock(id=1, full_name="Test Reader")
    mock_book_repo.get_by_id.return_value = Mock(id=1, title="Test Book", quantity=0)
    
    #создаем сервис
    service = BorrowingService(mock_borrowing_repo, mock_book_repo, mock_reader_repo)
    
    # вызываем метод и ожидаем ошибку
    borrowing_data = BorrowingCreate(reader_id=1, book_id=1, borrow_date=date.today())
    
    with pytest.raises(ValueError, match="Book is not available"):
        service.create_borrowing(borrowing_data)