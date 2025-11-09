import pandas as pd
from datetime import date
from typing import Generator, List
from app.models.borrowing import Borrowing
from app.repositories.borrowing_repository import BorrowingRepository

class ReportService:
    def __init__(self, borrowing_repository: BorrowingRepository):
        self.borrowing_repository = borrowing_repository

    def generate_overdue_report_data(self, report_date: date) -> Generator[dict, None, None]:
        """Генератор для обработки записей о просроченных книгах по одной"""
        borrowings: List[Borrowing] = self.borrowing_repository.get_overdue_borrowings(report_date)
        
        for borrowing in borrowings:
            days_overdue = (report_date - borrowing.borrow_date).days - 20
            if days_overdue > 0:
                yield {
                    "reader_name": borrowing.reader.full_name,
                    "book_title": borrowing.book.title,
                    "author": borrowing.book.author,
                    "borrow_date": borrowing.borrow_date,
                    "days_overdue": days_overdue
                }

    def create_overdue_report(self, report_date: date, format: str = "csv") -> bytes:
        """Создает отчет и возвращает его в виде bytes"""
        data = list(self.generate_overdue_report_data(report_date))
        if not data:
            # Возвращаем пустой отчет, если нет данных
            df = pd.DataFrame(columns=["reader_name", "book_title", "author", "borrow_date", "days_overdue"])
        else:
            df = pd.DataFrame(data)
        
        if format == "xlsx":
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Overdue Report')
            return output.getvalue()
        else:
            return df.to_csv(index=False).encode('utf-8')