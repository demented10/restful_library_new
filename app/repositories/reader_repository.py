from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.reader import Reader
from app.models.borrowing import Borrowing
from app.repositories.base_repository import BaseRepository

class ReaderRepository(BaseRepository[Reader]):
    def __init__(self, db: Session):
        super().__init__(Reader, db)

    def get_by_phone(self, phone: str)-> Optional[Reader]:
        return self.db.query(Reader).filter(Reader.phone == phone).first()
    
    def search_by_name(self, name: str) -> List[Reader]:
        return self.db.query(Reader).filter(Reader.full_name.ilike(f"%{name}")).all()
    
    def get_with_borrowings(self, reader_id: int) -> Optional[Reader]:
        return(
            self.db.query(Reader)
            .options(joinedload(Reader.borrowings).joinedload(Borrowing.book))
            .filter(Reader.id == reader_id)
            .first()
        )
    def get_active_borrowings_count(self, reader_id: int) -> int:
        return(
            self.db.query(Borrowing)
            .filter(Borrowing.reader_id == reader_id)
            .count()
        )