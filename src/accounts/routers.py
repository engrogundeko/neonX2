from fastapi import APIRouter, HTTPException, status, Depends

from typing import Annotated
from pydantic import BaseModel
from .models import Users
from fastapi.security import OAuth2PasswordRequestForm
from .auth import (hash_password, authenticate_user, get_access_token)
from .schema import (userIn, userOut)

from .schema import userIn

router = APIRouter()

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)

# class Token(BaseModel):
#     access_token: str
#     token_type: str

@router.post("/register")
async def create_user(user: userIn):
    user_dict = user.dict(exclude_unset = True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_obj = await Users.create(**user_dict)
    new_user = await userIn.from_tortoise_orm(user_obj)

    return (
        {
            "status": "ok",
            "message": f"user {new_user.username} has been created"
        }
    )

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return get_access_token(form_data.username)
