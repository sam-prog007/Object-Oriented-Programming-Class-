"""Data layer: an abstract repository (the contract) and an in-memory implementation."""

from abc import ABC, abstractmethod
from typing import Optional

from models import Book, BookIn


class BookRepository(ABC):
    @abstractmethod
    def list(self) -> list[Book]: ...

    @abstractmethod
    def get(self, book_id: int) -> Optional[Book]: ...

    @abstractmethod
    def add(self, data: BookIn) -> Book: ...

    @abstractmethod
    def update(self, book_id: int, data: BookIn) -> Optional[Book]: ...

    @abstractmethod
    def delete(self, book_id: int) -> bool: ...


class InMemoryBookRepository(BookRepository):
    """Stores books in a dict. A database version would implement the same ABC."""

    def __init__(self):
        self._books: dict[int, Book] = {}
        self._next_id = 1

    def list(self) -> list[Book]:
        return list(self._books.values())

    def get(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)

    def add(self, data: BookIn) -> Book:
        book = Book(id=self._next_id, **data.model_dump())
        self._books[book.id] = book
        self._next_id += 1
        return book

    def update(self, book_id: int, data: BookIn) -> Optional[Book]:
        if book_id not in self._books:
            return None
        self._books[book_id] = Book(id=book_id, **data.model_dump())
        return self._books[book_id]

    def delete(self, book_id: int) -> bool:
        return self._books.pop(book_id, None) is not None
