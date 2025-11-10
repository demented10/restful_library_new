"""
Скрипт для генерации фикстур
"""

import sys
import os
from datetime import date, timedelta
import random

# корневая директория проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.publisher import Publisher
from app.models.book import Book
from app.models.reader import Reader
from app.models.borrowing import Borrowing

# издатели
PUBLISHERS_DATA = [
    {"name": "Издатель тест_1", "city": "Тест_1 Город"},
    {"name": "Издатель тест_2", "city": "Тест_2 Город"},
    {"name": "Издатель тест_3", "city": "Тест_3 Город_"},
    {"name": "Издатель тест_4", "city": "Тест_4 Город"},
    {"name": "Издатель тест_5", "city": "Тест_5 Город"},
    {"name": "Издатель тест_6", "city": "Тест_6 Город"}
]

BOOKS_DATA = [
    {"title": "Книга тест_1", "author": "автор тест_1", "year": 2020, "price": 450, "quantity": 5},
    {"title": "Книга тест_2", "author": "автор тест_2", "year": 2019, "price": 520, "quantity": 31},
    {"title": "Книга тест_3", "author": "автор тест_3", "year": 1999, "price": 220, "quantity": 63},
    {"title": "Книга тест_4", "author": "автор тест_4", "year": 2019, "price": 530, "quantity": 32},
    {"title": "Книга тест_5", "author": "автор тест_5", "year": 2007, "price": 760, "quantity": 78},
    {"title": "Книга тест_6", "author": "автор тест_6", "year": 2019, "price": 130, "quantity": 1},
    {"title": "Книга тест_7", "author": "автор тест_7", "year": 2002, "price": 730, "quantity": 2},
    {"title": "Книга тест_8", "author": "автор тест_8", "year": 2012, "price": 990, "quantity": 3},
    {"title": "Книга тест_9", "author": "автор тест_9", "year": 2011, "price": 120, "quantity": 4},
    

]


READERS_DATA = [
    {"full_name": "Иванов Иван Иванович", "address": "ул. Ленина, д. 10, кв. 5", "phone": "+7-911-111-11-11"},
    {"full_name": "Петров Петр Петрович", "address": "ул. Пушкина, д. 25, кв. 12", "phone": "+7-922-222-22-22"},
    {"full_name": "Сидорова Мария Сергеевна", "address": "пр. Мира, д. 15, кв. 8", "phone": "+7-933-333-33-33"},
    {"full_name": "Кузнецов Алексей Владимирович", "address": "ул. Гагарина, д. 7, кв. 3", "phone": "+7-944-444-44-44"},
    {"full_name": "Смирнова Екатерина Дмитриевна", "address": "ул. Садовая, д. 30, кв. 15", "phone": "+7-955-555-55-55"},
    {"full_name": "Васильев Дмитрий Олегович", "address": "пр. Ленинградский, д. 45, кв. 22", "phone": "+7-966-666-66-66"},
    {"full_name": "Николаева Анна Павловна", "address": "ул. Центральная, д. 12, кв. 7", "phone": "+7-977-777-77-77"},
    {"full_name": "Орлов Сергей Викторович", "address": "ул. Молодежная, д. 8, кв. 4", "phone": "+7-988-888-88-88"},
]



def create_fixtures():
    """Создает тестовые данные в базе"""
    db = SessionLocal()
    
    try:
        print("Start fixture generation")
        
        # Очищаем существующие данные
        print("Clear exists data")
        db.query(Borrowing).delete()
        db.query(Book).delete()
        db.query(Reader).delete()
        db.query(Publisher).delete()
        db.commit()
        
        # Создаем издательства
        print("Create publishers")
        publishers = []
        for pub_data in PUBLISHERS_DATA:
            publisher = Publisher(**pub_data)
            db.add(publisher)
            publishers.append(publisher)
        
        db.commit()
        
        publisher_count = db.query(Publisher).count()
        print(f"Created {publisher_count} publishers")
        
        existing_publishers = db.query(Publisher).all()
        existing_publisher_ids = [p.id for p in existing_publishers]
        print(f"Existing publisher IDs: {existing_publisher_ids}")
        # Создаем книги
        print("Create books")
        books = []

        for book in BOOKS_DATA:            
            book_data = book.copy()
            book_data["publisher_id"] = random.choice(existing_publisher_ids)
            create_book = Book(**book_data)
            db.add(create_book)
            books.append(create_book)
        
        db.commit()
        print(f"Created {len(books)} books")
        
        # Создаем читателей
        print("Create readers")
        readers = []
        for reader_data in READERS_DATA:
            reader = Reader(**reader_data)
            db.add(reader)
            readers.append(reader)
        
        db.commit()
        print(f"Created {len(readers)} readers")
        
        #Создаем выдачи книг
        print("Creater book borrowings")
        borrowings_created = 0
        
        for reader in readers:
            # каждый читатель берет случайное количество книг (от 1 до 4)
            num_books_to_borrow = random.randint(1, 4)
            available_books = [b for b in books if b.quantity > 0]
            
            if len(available_books) < num_books_to_borrow:
                num_books_to_borrow = len(available_books)
            
            books_to_borrow = random.sample(available_books, num_books_to_borrow)
            
            for book in books_to_borrow:
                # Случайная дата выдачи (от 1 до 60 дней назад)
                days_ago = random.randint(1, 60)
                borrow_date = date.today() - timedelta(days=days_ago)
                
                borrowing = Borrowing(
                    reader_id=reader.id,
                    book_id=book.id,
                    borrow_date=borrow_date
                )
                db.add(borrowing)
                
                # уменьшаем количество доступных книг
                book.quantity -= 1
                borrowings_created += 1
        
        db.commit()
        print(f"Created {borrowings_created} book borrowings")
        
        # Выводим статистику
        print("Created data stats:")
        print(f"   Publishers: {len(publishers)}")
        print(f"   Books: {len(books)}")
        print(f"   Readers: {len(readers)}")
        print(f"   Borrowings: {borrowings_created}")
        
        # Показываем несколько просроченных выдач (если есть)
        overdue_date = date.today() - timedelta(days=20)
        overdue_borrowings = db.query(Borrowing).filter(Borrowing.borrow_date <= overdue_date).count()
        print(f"   overdue borrowings: {overdue_borrowings}")
        
        print("Fixture generation ended")
        
    except Exception as e:
        db.rollback()
        print(f"Fixture generation error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Fixture generator")
    create_fixtures()