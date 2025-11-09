from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.database import Base
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self) -> List[ModelType]:
        try:
            return self.db.query(self.model).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise

    def get_by_id(self, id: int) -> Optional[ModelType]:
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} by id {id}: {e}")
            raise

    def create(self, obj_in: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error creating {self.model.__name__}: {e}")
            raise ValueError(f"Foreign key constraint violation: {e}") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        try:
            db_obj = self.get_by_id(id)
            if db_obj:
                for field, value in obj_in.items():
                    setattr(db_obj, field, value)
                self.db.commit()
                self.db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error updating {self.model.__name__} {id}: {e}")
            raise ValueError(f"Foreign key constraint violation: {e}") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            raise

    def delete(self, id: int) -> bool:
        try:
            db_obj = self.get_by_id(id)
            if db_obj:
                self.db.delete(db_obj)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            raise

    def filter(self, **filters) -> List[ModelType]:
        try:
            query = self.db.query(self.model)
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error filtering {self.model.__name__}: {e}")
            raise