"""Slides 39-40: FastAPI is built on decorators.

- @app.get / @app.post / @app.put / @app.delete register a function as a route:
  no manual routing table, the decorator does it.
- Depends() injects shared logic into a route: here the repository (data access)
  and an API key check. Routes stay short and only contain business logic.

Run it:  uvicorn main:app --reload   then open http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI, Header, HTTPException, status

from models import Book, BookIn
from repository import BookRepository, InMemoryBookRepository

app = FastAPI(title="Library API", version="1.0")

API_KEY = "secret-dev-key"                 # demo only: a real app reads it from the environment
_repository = InMemoryBookRepository()     # one shared instance (module-level "singleton")


# ------------------------------------------------------------ dependencies ---
def get_repository() -> BookRepository:
    """Injected with Depends(); tests swap it with app.dependency_overrides."""
    return _repository


def require_api_key(x_api_key: str = Header(default=None)) -> None:
    """Write operations need the header  X-API-Key: secret-dev-key"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


# ------------------------------------------------------------------- routes ---
@app.get("/")
def home():
    return {"message": "Library API, see /docs"}


@app.get("/books", response_model=list[Book])
def list_books(repo: BookRepository = Depends(get_repository)):
    return repo.list()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, repo: BookRepository = Depends(get_repository)):
    book = repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(require_api_key)])
def create_book(data: BookIn, repo: BookRepository = Depends(get_repository)):
    return repo.add(data)


@app.put("/books/{book_id}", response_model=Book, dependencies=[Depends(require_api_key)])
def update_book(book_id: int, data: BookIn, repo: BookRepository = Depends(get_repository)):
    book = repo.update(book_id, data)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[Depends(require_api_key)])
def delete_book(book_id: int, repo: BookRepository = Depends(get_repository)):
    if not repo.delete(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
