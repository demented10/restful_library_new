from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.publisher import Publisher
from app.repositories.base_repository import BaseRepository

class PublisherRepository(BaseRepository[Publisher]):
    def __init__(self, db: Session):
        super().__init__(Publisher, db=db)

    def get_by_name(self, name: str) -> Optional[Publisher]:
        return self.db.query(Publisher).filter(Publisher.name == name).first()
    
    def get_by_city(self, city: str) -> List[Publisher]:
        return self.db.query(Publisher).filter(Publisher.city==city).all()