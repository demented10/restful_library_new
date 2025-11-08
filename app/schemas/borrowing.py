from pydantic import BaseModel
from datetime import date

class BorrowingBase(BaseModel):
    reader_id: int
    book_id: int
    borrow_date: date

class BorrowingCreate(BorrowingBase):
    pass

class Borrowing(BorrowingBase):
    id: int

    class Config:
        from_attributes = True