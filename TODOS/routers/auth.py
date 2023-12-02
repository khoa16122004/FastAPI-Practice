# import APIRouter
from fastapi import APIRouter

auth = APIRouter()

@auth.get("/auth/")
async def get_user():
    return {"user": "authenticated"}