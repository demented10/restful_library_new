from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.book import Book
from app.models.publisher import Publisher
from app.repositories.base_repository import BaseRepository

class BookRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Book, db)

    def get_all_with_publisher(self) -> List[Book]:
        return self.db.query(Book).options(joinedload(Book.publisher)).all()
    
    def get_by_id_with_publisher(self, id: int) -> Optional[Book]:
        return(
            self.db.query(Book)
            .options(joinedload(Book.publisher))
            .filter(Book.id == id)
            .first()
        )
    
    def search_books(self, query: str) -> List[Book]:
        return(
            self.db.query(Book)
            .options(joinedload(Book.publisher))
            .filter(
                or_(
                    Book.title.ilike(f"%{query}"),
                    Book.author.ilike(f"%{query}%")
                )
            )
            .all()
        )
    
    def get_by_author(self, author: str) -> List[Book]:
        return self.db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()
    
    def get_by_publisher(self, publisher_id: int) -> List[Book]:
        return self.db.query(Book).filter(Book.publisher_id == publisher_id).all()
    
    def get_available_books(self) -> List[Book]:
        return self.db.query(Book).filter(Book.quantity > 0).all()
    
    def decrease_quantity(self, book_id: int, amount: int = 1) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if book and book.quantity >= amount:
            book.quantity -= amount
            self.db.commit()
            self.db.refresh(book)
            return book
        return None
    
    def increase_quantity(self, book_id: int, amount: int = 1) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if book:
            book.quantity += amount
            self.db.commit()
            self.db.refresh(book)
            return book
        return None
