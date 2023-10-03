from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from accounts.models import Users

# from tortoise import Tortoise

import uuid


class Category(Model):
    id = fields.IntField(pk=True, index=True)
    # slug = fields.CharField(max_length=255, blank=True, null=True)
    name = fields.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(Model):
    # id = fields.IntField(pk=True)
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
    slug = fields.CharField(max_length=255, blank=True, null=True)
    name = fields.CharField(max_length=255)
    category = fields.ManyToManyField("models.Category", related_name="products")
    is_active = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.slug


class Brand(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=255)


class ProductInventory(Model):
    id = fields.IntField(pk=True, index=True)
    prod_asin = fields.CharField(max_length=50)
    product = fields.ForeignKeyField("models.Product")
    brand = fields.ForeignKeyField("models.Brand")
    is_active = fields.BooleanField()
    retail_price = fields.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    store_price = fields.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    is_on_sale = fields.BooleanField(default=True)
    is_digital = fields.BooleanField(default=False)
    weight = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product


class Stock(Model):
    id = fields.IntField(pk=True, index=True)
    # last_checked = fields.
    unit = fields.BigIntField()
    units_sold = fields.IntField()
    product_inventory = fields.OneToOneField("models.ProductInventory")

    def __str__(self) -> str:
        return self.unit


class Media(Model):
    id = fields.IntField(pk=True, index=True)
    img_url = fields.CharField(max_length=500, blank=False, null=False)
    alt_text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    product_inventory = fields.ForeignKeyField("models.ProductInventory")

    def __str__(self):
        return self.img_url


class UserCart(Model):
    id = fields.IntField(pk=True, index=True)
    user_id = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)


class CartItems(Model):
    id = fields.IntField(pk=True, index=True)
    cart_id = fields.ForeignKeyField("models.UserCart")
    product_id = fields.ForeignKeyField("models.ProductInventory")
    quantity = fields.IntField()

    def __str__(self) -> str:
        return self.cart_id
