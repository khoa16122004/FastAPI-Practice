# import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # instace to hashing password

# validation User request
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# param means: db will be define in a "get_db" function        
db_dependency = Annotated[Session, Depends(get_db)]    



@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # this following line will not work cause Users table doesnt have "passwork" atribute
    # create_user_model = Users(**create_user_request.model_dump()) # create Users instance database
    
    create_user_model = Users(email=create_user_request.email,
                                username=create_user_request.username,
                                first_name=create_user_request.first_name,
                                last_name=create_user_request.last_name,
                                role=create_user_request.role,
                                hashed_password=bcrypt_context.hash(create_user_request.password),
                                is_active=True)
    
    db.add(create_user_model) # insert
    db.commit() # commit insert process
    
# @router.get("/auth/read_all")
# async def auth_read_all(db: db_dependency):
#     return db.query(Users).all()
    