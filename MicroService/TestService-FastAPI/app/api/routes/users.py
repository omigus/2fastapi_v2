
from typing import List
from starlette.responses import JSONResponse
from fastapi import FastAPI, Header, Response, APIRouter, Body
from app.models.users import users,User
from app.db.events import connect_db
import logging

router = APIRouter()

@router.get("/users" , response_model=List[User])
async def read_root():
    query = users.select()
    return await connect_db().fetch_all(query)
  
