from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index = True, nullable=False)  
    city = Column(String, nullable=False)

    books = relationship("Book", back_populates="publisher")