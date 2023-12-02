from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=2000)
    class Config:
        schema_extra =  {
            "example":{
                "title": "ML for student",
                "author": "Tran Woffy",
                "description": "A new book for machine learning",
                "rating": 5,
                "published_date": 2005
                }
            }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5,2004),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5,2012),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5,2017),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2,2019),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3,2022),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1,2015)
]


@app.get("/books", status_code=status.HTTP_200_OK) # successfull rq - data return
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK) # successfull rq - data return
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    # handle epxect if we dont book id not exist
    # for invalid value from client using 404 error
    raise HTTPException(status_code=404, detail="Item Book not found")


@app.get("/books/by_rating/", status_code=status.HTTP_200_OK) # successfull rq - data return
async def read_book_by_rating(book_rating: int = Query(lt=6)):
    books_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_return.append(book)
    return books_return

# assingemnent
@app.get("/books/publish/", status_code=status.HTTP_200_OK) # successfull rq - data return
async def read_book_by_years(years: int = Query(gt=2000)):
    book_result = []
    for book in BOOKS:
        if book.published_date == years:
            book_result.append(book)
    return book_result



@app.post("/create-book", status_code=status.HTTP_202_ACCEPTED) # successful rq - crreate new data
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT) # successfull rq - no data return 
async def upadate_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            BOOKS[i] = book
            book_changed = True

    
    # handle epxect if we dont book id not exist
    # for invalid value from client using 404 error
    if not book_changed:
        raise HTTPException(status_code=404, detail="There aren't anybook mactch your input")



@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT) # successfull rq - no data return 
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    # handle epxect if we dont book id not exist
    # for invalid value from client using 404 error
    if  not book_changed:
        raise HTTPException(status_code=404, detail="There aren't anybook match your input")
