from typing import List, Optional
from app.models.publisher import Publisher
from app.repositories.publisher_repository import PublisherRepository
from app.schemas.publisher import PublisherCreate, PublisherUpdate
from app.services.base_service import BaseService

class PublisherService(BaseService[Publisher, PublisherCreate, PublisherUpdate]):
    def __init__(self, publisher_repository: PublisherRepository):
        super().__init__(publisher_repository)
        self.publisher_repository = publisher_repository

    def get_by_name(self, name: str) -> Optional[Publisher]:
        return self.publisher_repository.get_by_name(name)

    def get_by_city(self, city: str) -> List[Publisher]:
        return self.publisher_repository.get_by_city(city)