from fastapi import FastAPI
from accounts.models import Users
from inventory.models import (
    Product,
    ProductInventory,
    Stock,
    Brand,
    Media,
    CartItems,
    UserCart,
    Category,
)
from accounts.routers import router as account_router
from inventory.routers import router as inventory_router

import accounts
import inventory

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


app.include_router(account_router)
app.include_router(inventory_router)


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["accounts.models", "inventory.models"]},
    generate_schemas=True,  # This generates the database schema
    add_exception_handlers=True,  # Add exception handlers to FastAPI
)
