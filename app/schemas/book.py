from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    year: str
    price: int
    quantity: int
    publisher_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    publisher_id: Optional[int]

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
        