from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key= True, index= True)
    title = Column(String, nullable=False, index = True)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable= False)
    price = Column(Integer, nullable= False)
    quantity = Column(Integer, default= 1)

    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)

    publisher = relationship("Publisher", back_populates="books")
    borrowings = relationship("Borrowing", back_populates="book")