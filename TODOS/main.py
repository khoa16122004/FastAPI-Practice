from fastapi import FastAPI
import models
from routers import auth, todo
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine) # create all table
# turn on the cmd: sqlite3 todos.db

app.include_router(auth.router)
app.include_router(todo.router)
