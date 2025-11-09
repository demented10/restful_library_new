from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.services.publisher_service import PublisherService
from app.schemas.publisher import Publisher, PublisherCreate, PublisherUpdate
from app.api.dependencies import get_publisher_service

router = APIRouter(prefix="/publishers", tags=["publishers"])


@router.get("/", response_model=List[Publisher])
def get_publishers(
    service: PublisherService = Depends(get_publisher_service),
):
    """Получить все издательства"""
    return service.get_all()


@router.get("/{publisher_id}", response_model=Publisher)
def get_publisher(
    publisher_id: int,
    service: PublisherService = Depends(get_publisher_service),
):
    """Получить издательство по id"""
    publisher = service.get_by_id(publisher_id)
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )
    return publisher


@router.post("/", response_model=Publisher, status_code=status.HTTP_201_CREATED)
def create_publisher(
    publisher: PublisherCreate,
    service: PublisherService = Depends(get_publisher_service),
):
    """Создать новое издательство"""
    return service.create(publisher)


@router.put("/{publisher_id}", response_model=Publisher)
def update_publisher(
    publisher_id: int,
    publisher_update: PublisherUpdate,
    service: PublisherService = Depends(get_publisher_service),
):
    """Обновить издательство"""
    publisher = service.update(publisher_id, publisher_update)
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )
    return publisher


@router.delete("/{publisher_id}")
def delete_publisher(
    publisher_id: int,
    service: PublisherService = Depends(get_publisher_service),
):
    """Удалить издательство"""
    if not service.delete(publisher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )
    return {"message": "Publisher deleted successfully"}
