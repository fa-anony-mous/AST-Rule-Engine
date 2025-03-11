import sys
import os
import atexit
import asyncio
import signal
from contextlib import asynccontextmanager

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.settings import settings
from app.core.db import engine, cleanup_db_resources

# Function to run cleanup in a new event loop
def dispose_db_sync():
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(cleanup_db_resources())
        loop.close()
    except Exception as e:
        print(f"Error during sync cleanup: {e}")

# Register the cleanup function to run at exit
atexit.register(dispose_db_sync)

# For handling SIGTERM in containerized environments
def handle_sigterm(*args):
    dispose_db_sync()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Nothing special needed
    yield
    # Shutdown: Explicitly dispose engine
    try:
        await cleanup_db_resources()
    except Exception as e:
        print(f"Error in lifespan cleanup: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
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