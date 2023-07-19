from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# API endpoint definition: respone in htpps::..../api-endponts

## get request
@app.get("/books/")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "my favorite book"}

        
@app.get("/books/")
async def read_category_by_querry(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_querry(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author and book.get("category") == category:
            books_to_return.append(book)
    return books_to_return

## post request
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

## put request
@app.put("/books/update_book")
async def update_book(new_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == new_book.get("title").casefold():
            BOOKS[i] = new_book

# delete request
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            return "Khoa"
        

# assignment 1: Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters

# Path parameters
@app.get("/books/find_author/{author}")
async def find_books_author(author: str):
    book_find = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            book_find.append(book)
    return book_find

## querry
@app.get("/books/find_author/")
async def find_book_author(author: str):
    book_find = []
    for book in BOOKS:
            if book.get("author").casefold() == author.casefold():
                book_find.append(book)
                print("Khoa")
    return book_find

