import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from typing import Annotated
from pydantic import BaseModel
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .models import Users
from .schema import users

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


async def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = Users(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# async def get_user_by_username(username: str):
#     try:
#         user = await users.from_queryset_single(Users.get(username=username))
#         return user
#     except Exception as e:
#         raise HTTPException({"details":str()})


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# print(Users.get(id=1))


async def authenticate_user(username: str, password: str):
    try:
        user = await Users.get(username=username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        return False


def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        # print(expire)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        # print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(username):
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = _create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# async def get_current_active_user(
#     current_user: Annotated[user, Depends(get_current_user)]
# ):
#     return current_user
