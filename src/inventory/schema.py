from tortoise.contrib.pydantic import pydantic_model_creator
from .models import *

# category_pydantic = pydantic_model_creator(Category, name="Category")
category_pydanticIn = pydantic_model_creator(
    Category, name="CategoryIn", exclude_readonly=True
)
category_pydanticOut = pydantic_model_creator(Category, name="CategoryOut")

product_pydanticIn = pydantic_model_creator(
    Product, name="Product", exclude=("uuid, created_at, updated_at")
)
product_pydanticOut = pydantic_model_creator(
    Product,
    name="ProductOut",
)

brand_pydanticIn = pydantic_model_creator(Brand, name="BrandIn", exclude=("id,"))
brand_pydanticOut = pydantic_model_creator(Brand, name="BrandOut")

product_inventory_pydanticIn = pydantic_model_creator(
    ProductInventory, name="ProductInventoryIn", exclude_readonly=True
)
product_inventory_pydanticOut = pydantic_model_creator(
    ProductInventory, name="ProductInventoryOut", exclude=("id",)
)


stock_pydanticIn = pydantic_model_creator(Stock, name="StockIn", exclude_readonly=True)
stock_pydanticOut = pydantic_model_creator(
    Stock, name="StockOut", exclude_readonly=True
)


media_pydantic = pydantic_model_creator(Media, name="MediaIn", exclude_readonly=True)
media_pydantic = pydantic_model_creator(Media, name="MediaOut", exclude=("id",))

user_cart_pydanticIn = pydantic_model_creator(
    UserCart, name="UserCartIn", exclude_readonly=True
)
user_cart_pydanticOut = pydantic_model_creator(
    UserCart, name="UserCart", exclude=("id",)
)

cart_items_pydanticIn = pydantic_model_creator(
    CartItems, name="CartItem", exclude_readonly=True
)
cart_items_pydanticOut = pydantic_model_creator(
    CartItems, name="CartItemOut", exclude_readonly=True
)
