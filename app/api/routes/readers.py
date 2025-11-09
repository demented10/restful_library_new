from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.services.reader_service import ReaderService
from app.schemas.reader import Reader, ReaderCreate, ReaderUpdate
from app.api.dependencies import get_reader_service

router = APIRouter(prefix="/readers", tags=["readers"])

@router.get("/", response_model=List[Reader])
def get_readers(
    service: ReaderService = Depends(get_reader_service),
):
    """Получить всех читателей"""
    return service.get_all()

@router.get("/{reader_id}", response_model=Reader)
def get_reader(
    reader_id: int,
    service: ReaderService = Depends(get_reader_service),
):
    """Получить читателя по Id"""
    reader = service.get_by_id(reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return reader

@router.get("/{reader_id}/with-borrowings", response_model=Reader)
def get_reader_with_borrowings(
    reader_id: int,
    service: ReaderService = Depends(get_reader_service),
):
    """Получить читателя с информацией о выданных книгах"""
    reader = service.get_with_borrowings(reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return reader

@router.get("/search/", response_model=List[Reader])
def search_readers(
    name: str = Query(..., min_length=1, description="Поиск по ФИО"),
    service: ReaderService = Depends(get_reader_service),
):
    """Поиск читателей по ФИО"""
    return service.search_by_name(name)

@router.get("/phone/{phone}", response_model=Reader)
def get_reader_by_phone(
    phone: str,
    service: ReaderService = Depends(get_reader_service),
):
    """Получить читателя по номеру телефона"""
    reader = service.get_by_phone(phone)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return reader

@router.post("/", response_model=Reader, status_code=status.HTTP_201_CREATED)
def create_reader(
    reader: ReaderCreate,
    service: ReaderService = Depends(get_reader_service),
):
    """Создать нового читателя"""
    # Проверяем, нет ли уже читателя с таким телефоном
    existing_reader = service.get_by_phone(reader.phone)
    if existing_reader:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reader with this phone already exists"
        )
    return service.create(reader)

@router.put("/{reader_id}", response_model=Reader)
def update_reader(
    reader_id: int,
    reader_update: ReaderUpdate,
    service: ReaderService = Depends(get_reader_service),
):
    """Обновить читаетля"""
    reader = service.update(reader_id, reader_update)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return reader

@router.delete("/{reader_id}")
def delete_reader(
    reader_id: int,
    service: ReaderService = Depends(get_reader_service),
):
    """Удалить читателя"""
    if not service.delete(reader_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return {"message": "Reader deleted successfully"}