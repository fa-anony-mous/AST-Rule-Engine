from fastapi import FastAPI
from app.core.db import SessionLocal  # Import SessionLocal from db.py
from app.api.v1.router import api_router

app = FastAPI()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Export SessionLocal for use in other modules
__all__ = ["SessionLocal"] 