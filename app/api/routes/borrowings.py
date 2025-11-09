from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from app.services.borrowing_service import BorrowingService
from app.schemas.borrowing import Borrowing, BorrowingCreate
from app.api.dependencies import get_borrowing_service

router = APIRouter(prefix="/borrowings", tags=["borrowings"])

@router.get("/", response_model=List[Borrowing])
def get_borrowings(
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить все выдачи книг с детальной информацией"""
    return service.get_all_with_details()

@router.get("/{borrowing_id}", response_model=Borrowing)
def get_borrowing(
    borrowing_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить выдачу по ID"""
    borrowing = service.get_by_id(borrowing_id)
    if not borrowing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowing record not found"
        )
    return borrowing

@router.get("/reader/{reader_id}", response_model=List[Borrowing])
def get_borrowings_by_reader(
    reader_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить выдачи по читателю"""
    return service.get_by_reader(reader_id)

@router.get("/book/{book_id}", response_model=List[Borrowing])
def get_borrowings_by_book(
    book_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить выдачи по книге"""
    return service.get_by_book(book_id)

@router.get("/active/", response_model=List[Borrowing])
def get_active_borrowings(
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить активные выдачи"""
    return service.get_active_borrowings()

@router.get("/overdue/", response_model=List[Borrowing])
def get_overdue_borrowings(
    check_date: Optional[date] = Query(None, description="Дата для проверки просрочки (по умолчанию сегодня)"),
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Получить просроченные выдачи"""
    return service.get_overdue_borrowings(check_date)

@router.post("/", response_model=Borrowing, status_code=status.HTTP_201_CREATED)
def create_borrowing(
    borrowing: BorrowingCreate,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Создать новую выдачу книги"""
    try:
        return service.create_borrowing(borrowing)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{borrowing_id}/return")
def return_book(
    borrowing_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Вернуть книгу (удалить запись о выдаче)"""
    try:
        success = service.return_book(borrowing_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Borrowing record not found"
            )
        return {"message": "Book returned successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )