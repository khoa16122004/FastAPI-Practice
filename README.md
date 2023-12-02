# Hello world to Backend

## API Execution:
To run the API file, use the following command:

        uvicorn <file_name>:app --reload


## Request Methods:
- **GET**: `/books/` {path parameter}
- **QUERY**: `/books/?category=science` (query parameter)
- **POST**: Create new data
- **PUT**: Update existing data
- **DELETE**: Remove data

Note: When using the **GET** method, the query parameter should follow the endpoint.

## Validation Values:

- **Using in atribute**:
  ```python
  class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=2000)

- **GET**: Path method
  ```python
  async def get_validation(param: int = Path(lt=2)):

- **QUERY**: Query method
  ```python
  async def get_validation(param: int = Query(lt=2)):

## Status Codes:
### 2xx series - Standard Response of a Successful Request:
- **200 - OK**: Commonly used for `GET` requests when data is returned.
- **202 - Created**: Successful request for creating new data. Commonly used for `POST` requests.
- **204 - No Content**: Successful request, but no content is returned (null). Example: `PUT` request.

### 4xx series - Client Errors:
- **400 - Bad Request**: Unable to process the request due to a client error. Commonly used for invalid methods, such as an incorrect HTTP method.
- **401 - Unauthorized**: Authentication failed or the user does not have permission to access.
- **404 - Not Found**: The requested resource or endpoint cannot be found.
- **422 - Unprocessable Entity**: Invalid constraints from the client.

### 5xx series - Server Status Codes:
- **500 - Internal Server Error**: Occurs when an unexpected issue happens on the server.

## Raise exeption
  ```python
  from fastapi imort HTTPExeption

  @app.get(....)
  async def somethint():
    # your code
    ...
    raise HTTPExeption(status_code="404", detail="your warn")    
  ``````
## Explicit Status code
 
  ```python
  from starlette import status

  @app.get("/books", status_code=status.HTPP_200_OK) 
  @app.get("/books/create_book", status_code=status.HTPP_202_CREATED) 
  @app.get("/books", status_code=status.HTPP_204_NO_CONTENT) 
  ```


# Database with API

## SQL Alchemy
This a modul in python helping us for connect and control with database easily through a injection code. This following code for create a simple setup for **sqlalchemy**

  ```python
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker
  from sqlalchemy.ext.declarative import declarative_base

  SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db" #

  engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) # connect with database through URL


  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # UI to interact with Database

  Base = declarative_base() # class stand for table
  ```
  In another file, just import  **Base** and it's will create a file with ext == **.db**, after this run commandline: 

    sqlite3 todos.db

