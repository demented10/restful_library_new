from typing import List, Optional
from app.repositories.reader_repository import ReaderRepository
from app.models import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate
from app.services.base_service import BaseService

class ReaderService(BaseService[Reader, ReaderCreate, ReaderUpdate]):
    def __init__(self, reader_repository: ReaderRepository):
        super().__init__(reader_repository)
        self.reader_repository = reader_repository

    def get_by_phone(self, phone: str) -> Optional[Reader]:
        return self.reader_repository.get_by_phone(phone)

    def search_by_name(self, name: str) -> List[Reader]:
        return self.reader_repository.search_by_name(name)

    def get_with_borrowings(self, reader_id: int) -> Optional[Reader]:
        return self.reader_repository.get_with_borrowings(reader_id)

    def get_active_borrowings_count(self, reader_id: int) -> int:
        return self.reader_repository.get_active_borrowings_count(reader_id)