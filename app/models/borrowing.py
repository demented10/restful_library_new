from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, index = True, primary_key= True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable = False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable= False)
    borrow_date = Column(Date, default=date.today, nullable = False)

    reader = relationship("Reader", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
