from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.borrowing import Borrowing
from app.repositories.base_repository import BaseRepository

class BorrowingRepository(BaseRepository[Borrowing]):
    def __init__(self, db: Session):
        super().__init__(Borrowing, db)

    def get_all_with_details(self)-> List[Borrowing]:
        return(
            self.db.query(Borrowing)
            .options(
                joinedload(Borrowing.reader),
                joinedload(Borrowing.book).joinedload("publisher")
            )
            .all()
        )
    
    def get_by_id_with_details(self, id: int) -> Optional[Borrowing]:
        return(
            self.db.query(Borrowing)
            .options(
                joinedload(Borrowing.reader),
                joinedload(Borrowing.book).joinedload("publisher")
            )
            .filter(Borrowing.id == id)
            .first()
        )
    
    def get_by_reader(self, reader_id: int) -> List[Borrowing]:
        return(
            self.db.query(Borrowing)
            .options(joinedload(Borrowing.book))
            .filter(Borrowing.reader_id == reader_id)
            .all()
        )
    
    def get_by_book(self, book_id: int) -> List[Borrowing]:
        return self.db.query(Borrowing).filter(Borrowing.book_id == book_id).all()
    
    def get_active_borrowings(self) -> List[Borrowing]:
        return(
            self.db.query(Borrowing)
            .options(
                joinedload(Borrowing.reader),
                joinedload(Borrowing.book)
            )
            .all()
        )
    
    def get_overdue_borrowings(self, check_date: date = None) -> List[Borrowing]:
        if check_date is None:
            check_date = date.today()
        
        max_days = 20
        overdue_date = check_date - timedelta(days=max_days)

        return(
            self.db.query(Borrowing)
            .options(
                joinedload(Borrowing.reader),
                joinedload(Borrowing.book)
            )
            .filter(Borrowing.borrow_date <= overdue_date)
            .all()
        )
    
    def get_borrowing_by_date_range(self, start_date: date, end_date: date) -> List[Borrowing]:
        return(
            self.db.query(Borrowing)
            .options(
                joinedload(Borrowing.reader),
                joinedload(Borrowing.book)
            )
            .filter(
                and_(
                    Borrowing.borrow_date >= start_date,
                    Borrowing.borrow_date <= end_date
                )
            )
            .all()
        )
    
    def get_reader_active_borrowings_count(self, reader_id: int) -> int:
        return(
            self.db.query(Borrowing)
            .filter(Borrowing.reader_id == reader_id)
            .count()
        )
