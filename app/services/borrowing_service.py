from typing import List, Optional
from datetime import date
from app.models.borrowing import Borrowing
from app.models.book import Book
from app.models.reader import Reader
from app.repositories.borrowing_repository import BorrowingRepository
from app.repositories.book_repository import BookRepository
from app.repositories.reader_repository import ReaderRepository
from app.schemas.borrowing import BorrowingCreate
from app.services.base_service import BaseService


class BorrowingService(BaseService[Borrowing, BorrowingCreate, BorrowingCreate]):
    def __init__(
        self,
        borrowing_repository: BorrowingRepository,
        book_repository: BookRepository,
        reader_repository: ReaderRepository,
    ):
        super().__init__(borrowing_repository)
        self.borrowing_repository = borrowing_repository
        self.book_repository = book_repository
        self.reader_repository = reader_repository

    def create_borrowing(self, borrowing_in: BorrowingCreate) -> Optional[Borrowing]:
        # Проверяем, существует ли читатель
        reader = self.reader_repository.get_by_id(borrowing_in.reader_id)
        if not reader:
            raise ValueError("Reader not found")

        # Проверяем, существует ли книга
        book = self.book_repository.get_by_id(borrowing_in.book_id)
        if not book:
            raise ValueError("Book not found")

        # Проверяем, доступно ли количество книг
        if book.quantity < 1:
            raise ValueError("Book is not available")

        # Проверяем, не превышает ли читатель лимит в 5 книг
        active_borrowings = (
            self.borrowing_repository.get_reader_active_borrowings_count(
                borrowing_in.reader_id
            )
        )
        if active_borrowings >= 5:
            raise ValueError("Reader cannot borrow more than 5 books")

        # Уменьшаем количество доступных книг
        self.book_repository.decrease_quantity(book.id, 1)

        # Создаем запись о выдаче
        borrowing_data = borrowing_in.model_dump()
        return self.borrowing_repository.create(borrowing_data)

    def return_book(self, borrowing_id: int) -> bool:
        borrowing = self.borrowing_repository.get_by_id(borrowing_id)
        if not borrowing:
            raise ValueError("Borrowing record not found")

        # Увеличиваем количество доступных книг
        self.book_repository.increase_quantity(int(borrowing.book_id), amount=1)

        # Удаляем запись о выдаче
        return self.borrowing_repository.delete(borrowing_id)

    def get_all_with_details(self) -> List[Borrowing]:
        return self.borrowing_repository.get_all_with_details()

    def get_by_reader(self, reader_id: int) -> List[Borrowing]:
        return self.borrowing_repository.get_by_reader(reader_id)

    def get_by_book(self, book_id: int) -> List[Borrowing]:
        return self.borrowing_repository.get_by_book(book_id)

    def get_active_borrowings(self) -> List[Borrowing]:
        return self.borrowing_repository.get_active_borrowings()

    def get_overdue_borrowings(self, check_date : Optional[date]  = None) -> List:
        return self.borrowing_repository.get_overdue_borrowings(check_date)

    def get_reader_active_borrowings_count(self, reader_id: int) -> int:
        return self.borrowing_repository.get_reader_active_borrowings_count(reader_id)
