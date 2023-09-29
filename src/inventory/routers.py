from fastapi import APIRouter

router = APIRouter()

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)