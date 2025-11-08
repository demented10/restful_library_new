from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index = True)
    full_name = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    borrowings = relationship("Borrowing", back_populates="reader")
