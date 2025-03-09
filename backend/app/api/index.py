from fastapi import FastAPI
from .v1.router import router as api_router  # Import your existing router

app = FastAPI()

# Include your existing routes
app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}
