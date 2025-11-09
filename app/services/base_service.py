from typing import List, Optional, TypeVar, Generic
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType') 
UpdateSchemaType = TypeVar('UpdateSchemaType')

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_all(self) -> List[ModelType]:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.repository.get_by_id(id)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        return self.repository.create(obj_in_data)

    def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        return self.repository.update(id, obj_in_data)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)