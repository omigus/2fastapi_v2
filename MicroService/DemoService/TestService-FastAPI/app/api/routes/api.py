  
from fastapi import APIRouter
from app.api.routes import users

def run_router(app):
    app.include_router(
      users.router,
      prefix="/api/v2",
      tags=["users"],
      responses={404: {"message": "Not found"}},
  )