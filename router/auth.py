from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt


router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)


SECRET_KEY = "5O9+OrLo19dsYuwOA1Y3GweRXSm2KT+5CVNbLcH+vAw="
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')



class Create_User_Request(BaseModel):
    username : str
    email : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def Authenticate_user(user_name : str, password : str, db):
    user = db.query(Users).filter(Users.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(user_name : str, user_id : int, expires_delta : timedelta):
    encode = {'sub' : user_name, 'id' : user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)



async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user_name : str = payload.get('sub')
        user_id : int = payload.get('id')

        if user_name is None or user_id is None :
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Couldn't validate the user")
        return{'user_name' : user_name, 'id' : user_id}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Couldn't validate the user")
    



@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_new_user(db : db_dependency, user : Create_User_Request):
    user = Users(
        user_name = user.username,
        email = user.email,
        hashed_password = bcrypt_context.hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user) 




@router.post("/token", status_code = status.HTTP_201_CREATED)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):   
    user = Authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate the user")
    token = create_access_token(user.user_name, user.id, timedelta(minutes = 20))
    return {"access_token" : token, "token_type" : "Bearer"}