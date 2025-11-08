from pydantic import BaseModel
from typing import Optional

class PublisherBase(BaseModel):
    name: str
    city: str

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None

class Publisher(PublisherBase):
    id: int

    class Config:
        from_attributes = True


