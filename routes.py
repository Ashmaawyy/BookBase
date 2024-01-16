from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Book, BookUpdate

router = APIRouter()

@router.post("/", response_description = "Create a new book", \
             status_code = status.HTTP_201_CREATED, response_model = Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book

@router.get("/", response_description = "List all books", response_model = List[Book])
def list_books(request: Request):
    books = list(request.app.database["books"].find(limit=100))
    return books