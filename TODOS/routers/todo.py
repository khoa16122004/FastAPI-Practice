from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from models import Todo
from sqlalchemy.orm import Session

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# param means: db will be define in a "get_db" function        
db_dependency = Annotated[Session, Depends(get_db)]    


# validation Todo request
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool



@router.get("/",  status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency,):
    return db.query(Todo).all() # select * from todo
    
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    # check if exist
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first() # selection from where
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail='Todo not found')

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todo(**todo_request.model_dump()) # create Todo instance database
    db.add(todo_model) # insert
    db.commit() # commit insert process
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_id: int,
                      todo_request: TodoRequest):
    # check if exist
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found. ")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    # check if exist
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()
    
    db.commit()



