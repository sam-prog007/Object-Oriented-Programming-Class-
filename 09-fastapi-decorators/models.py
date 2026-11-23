"""Pydantic models: FastAPI uses them to validate request bodies automatically."""

from pydantic import BaseModel, Field


class BookIn(BaseModel):
    """What a client sends."""

    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=0, le=2100)


class Book(BookIn):
    """What the API returns: the same fields plus an id."""

    id: int
