from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=255, null=False, unique=True)
    email = fields.CharField(max_length=255, null=False, unique=True)
    password = fields.CharField(max_length=50, null=False)
    is_verified = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    joined_date = fields.DatetimeField(auto_now_add=True)
