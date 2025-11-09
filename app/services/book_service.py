from typing import List, Optional
from app.models import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate
from app.services.base_service import BaseService

class BookService(BaseService[Book, BookCreate, BookUpdate]):
    def __init__(self, book_repository: BookRepository):
        super().__init__(book_repository)
        self.book_repository = book_repository

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