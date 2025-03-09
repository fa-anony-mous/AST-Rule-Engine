from fastapi import APIRouter
from .endpoints import rules

api_router = APIRouter()

api_router.include_router(
    rules.router,
    prefix="/rules",
    tags=["Rules"]
)

