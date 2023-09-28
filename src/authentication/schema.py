from tortoise.contrib.pydantic import pydantic_model_creator
from .models import *

user = pydantic_model_creator(Users, name="User")
userIn = pydantic_model_creator(
    Users, name="UserIn", exclude=("id", "is_verified", "is_admin", "joined_date")
)
userOut = pydantic_model_creator(Users, namme="UserOut", exclude=("password", "is_verified", "is_admin",))
