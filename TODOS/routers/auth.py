# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext # for hash password
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime

router = APIRouter()

SECRET_KEY = '5d3711a26b488b38642c948a7bc8fa09fe9ba78a2d6b57cac46a34bb0f840147' # key from unique user
ALGORITHM = "HS256" # algorithm


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # instace to hashing password

# validation User request
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "admin"
    

class Token(BaseModel):
    access_token: str
    token_type: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def add_database(db, request):
    try:
        db.add(request)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    
# param means: db will be define in a "get_db" function        
db_dependency = Annotated[Session, Depends(get_db)]    

# Check auth sucessfully
def authenticate_user(username: str, password: str, db):
    # find the user infomration if exist
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    # the password not match
    if not bcrypt_context.verify(password, user.hashed_password): # compare beetween input and database
        return False
    
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth")
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # this following line will not work cause Users table doesnt have "passwork" atribute
    # create_user_model = Users(**create_user_request.model_dump()) # create Users instance database
    
    create_user_model = Users(email=create_user_request.email,
                                username=create_user_request.username,
                                first_name=create_user_request.first_name,
                                last_name=create_user_request.last_name,
                                role=create_user_request.role,
                                hashed_password= bcrypt_context.hash(create_user_request.password),
                                is_active=True)
    
    
    db.add(create_user_model) # insert
    db.commit() # commit insert process
    
    
    return {"Status":"Successfully created"}
    
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, "token_type": "bearer"}

@router.get("/authentic_all")
async def take_all_user(db: db_dependency):
    return db.query(Users).all()


@router.get("/test")
async def test():
    return "concac"

