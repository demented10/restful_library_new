from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.services.book_service import BookService
from app.schemas.book import Book, BookCreate, BookUpdate
from app.api.dependencies import get_book_service

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
def get_books(
    service: BookService = Depends(get_book_service),
):
    """Получить все книги"""
    return service.get_all()

@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    """Получить книгу по id"""
    book = service.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.get("/{book_id}/with-publisher", response_model=Book)
def get_book_with_publisher(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    """Получить книгу с информацией об издательстве"""
    book = service.get_by_id_with_publisher(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.get("/search/", response_model=List[Book])
def search_books(
    query: str = Query(..., min_length=1, description="Поиск по названию или автору"),
    service: BookService = Depends(get_book_service),
):
    """Поиск книг по названию или автору"""
    return service.search_books(query)

@router.get("/author/{author}", response_model=List[Book])
def get_books_by_author(
    author: str,
    service: BookService = Depends(get_book_service),
):
    """Получить книги по автору"""
    return service.get_by_author(author)

@router.get("/publisher/{publisher_id}", response_model=List[Book])
def get_books_by_publisher(
    publisher_id: int,
    service: BookService = Depends(get_book_service),
):
    """Получить книги по издательству"""
    return service.get_by_publisher(publisher_id)

@router.get("/available/", response_model=List[Book])
def get_available_books(
    service: BookService = Depends(get_book_service),
):
    """Получить доступные книги (в наличии)"""
    return service.get_available_books()

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service),
):
    """Создать новую книгу"""
    try:
        return service.create(book)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    service: BookService = Depends(get_book_service),
):
    """Обновить книгу"""
    try:
        book = service.update(book_id, book_update)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    """Удалить книгу"""
    if not service.delete(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return {"message": "Book deleted successfully"}