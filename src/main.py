from fastapi import FastAPI
from authentication.models import *
from inventory.models import *
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["authentication.models", "inventory.models"]},
    generate_schemas=True,  # This generates the database schema
    add_exception_handlers=True,  # Add exception handlers to FastAPI
)
