from pydantic import BaseModel
from typing import Optional

class ReaderBase(BaseModel):
    full_name: str
    address: str
    phone: str

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
        full_name: Optional[str]
        address: Optional[str]
        phone: Optional[str]

class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True