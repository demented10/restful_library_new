from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


