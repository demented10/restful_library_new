from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.publisher_repository import PublisherRepository
from app.repositories.book_repository import BookRepository
from app.repositories.reader_repository import ReaderRepository
from app.repositories.borrowing_repository import BorrowingRepository
from app.services.publisher_service import PublisherService
from app.services.book_service import BookService
from app.services.reader_service import ReaderService
from app.services.borrowing_service import BorrowingService
from app.services.report_service import ReportService

# Зависимости для репозиториев
def get_publisher_repository(db: Session = Depends(get_db)) -> PublisherRepository:
    return PublisherRepository(db)

def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return BookRepository(db)

def get_reader_repository(db: Session = Depends(get_db)) -> ReaderRepository:
    return ReaderRepository(db)

def get_borrowing_repository(db: Session = Depends(get_db)) -> BorrowingRepository:
    return BorrowingRepository(db)

# Зависимости для сервисов
def get_publisher_service(
    publisher_repo: PublisherRepository = Depends(get_publisher_repository)
) -> PublisherService:
    return PublisherService(publisher_repo)

def get_book_service(
    book_repo: BookRepository = Depends(get_book_repository)
) -> BookService:
    return BookService(book_repo)

def get_reader_service(
    reader_repo: ReaderRepository = Depends(get_reader_repository)
) -> ReaderService:
    return ReaderService(reader_repo)

def get_borrowing_service(
    borrowing_repo: BorrowingRepository = Depends(get_borrowing_repository),
    book_repo: BookRepository = Depends(get_book_repository),
    reader_repo: ReaderRepository = Depends(get_reader_repository)
) -> BorrowingService:
    return BorrowingService(borrowing_repo, book_repo, reader_repo)

def get_report_service(
    borrowing_repo: BorrowingRepository = Depends(get_borrowing_repository)
) -> ReportService:
    return ReportService(borrowing_repo)