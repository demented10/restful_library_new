DROP TABLE IF EXISTS publishers;
DROP TABLE IF EXISTS  books;
DROP TABLE IF EXISTS  borrowings;
DROP TABLE IF EXISTS  readers;


CREATE TABLE IF NOT EXISTS publishers(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    city VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS books(
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    price INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    publisher_id INTEGER NOT NULL REFERENCES publishers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS readers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    phone VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS borrowings(
    id SERIAL PRIMARY KEY,
    reader_id INTEGER NOT NULL REFERENCES readers(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    borrow_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_readers_name ON readers(full_name);
CREATE INDEX IF NOT EXISTS idx_borrowings_date ON borrowings(borrow_date);
CREATE INDEX IF NOT EXISTS idx_borrowings_reader ON borrowings(reader_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_book ON borrowings(book_id);