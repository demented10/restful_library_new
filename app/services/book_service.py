from typing import List, Optional
from app.models import Book
from app.repositories.book_repository import BookRepository
from app.repositories.publisher_repository import PublisherRepository
from app.schemas.book import BookCreate, BookUpdate
from app.services.base_service import BaseService

class BookService(BaseService[Book, BookCreate, BookUpdate]):
    def __init__(self, book_repository: BookRepository, publisher_repository: PublisherRepository):
        super().__init__(book_repository)
        self.book_repository = book_repository
        self.publisher_repository = publisher_repository

    def _validate_publisher(self, publisher_id: int) -> None:
        """Проверяет существование издателя"""
        publisher = self.publisher_repository.get_by_id(publisher_id)
        if not publisher:
            raise ValueError(f"Publisher with id {publisher_id} does not exist")

    def create(self, obj_in: BookCreate) -> Book:
        """Создает книгу с проверкой существования издателя"""
        self._validate_publisher(obj_in.publisher_id)
        
        obj_in_data = obj_in.model_dump()
        return self.book_repository.create(obj_in_data)

    def update(self, id: int, obj_in: BookUpdate) -> Optional[Book]:
        """Обновляет книгу с проверкой существования издателя (если он указан)"""
        if obj_in.publisher_id is not None:
            self._validate_publisher(obj_in.publisher_id)
        
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        return self.book_repository.update(id, obj_in_data)

    def get_all_with_publisher(self) -> List[Book]:
        return self.book_repository.get_all_with_publisher()

    def get_by_id_with_publisher(self, id: int) -> Optional[Book]:
        return self.book_repository.get_by_id_with_publisher(id)

    def search_books(self, query: str) -> List[Book]:
        return self.book_repository.search_books(query)

    def get_by_author(self, author: str) -> List[Book]:
        return self.book_repository.get_by_author(author)

    def get_by_publisher(self, publisher_id: int) -> List[Book]:
        return self.book_repository.get_by_publisher(publisher_id)

    def get_available_books(self) -> List[Book]:
        return self.book_repository.get_available_books()

    def decrease_quantity(self, book_id: int, amount: int = 1) -> Optional[Book]:
        return self.book_repository.decrease_quantity(book_id, amount)

    def increase_quantity(self, book_id: int, amount: int = 1) -> Optional[Book]:
        return self.book_repository.increase_quantity(book_id, amount)