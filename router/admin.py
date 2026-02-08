from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from URL_Shortner.models import URL
from URL_Shortner.database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from models import URL, Users


router = APIRouter(
    prefix = "/admin",
    tags = ["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]




@router.get("/admin/all_users")
async def get_all_users_in_db(user : user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "You are not an admin")
    user_model = db.query(Users).all()
