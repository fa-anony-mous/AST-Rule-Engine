import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.settings import settings


from contextlib import asynccontextmanager
from app.core.db import engines, EngineType

# Add this startup/shutdown handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Nothing special needed
    yield
    # Shutdown: Dispose all database engines
    for engine in engines.values():
        await engine.dispose()

# Update your FastAPI app creation
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan  # Add the lifespan handler
)
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in Development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include our API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Basic Health Check
@app.get("/health")
async def health_check():
    return {'status': 'ok'}


@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, port=8000)
    