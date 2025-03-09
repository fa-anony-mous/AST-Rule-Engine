from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "AST Rule Engine"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database URL
    POSTGRES_URL: str = "postgresql+asyncpg://postgres:saketh123@db.zfcqnzovzfgdogwlkzsj.supabase.co:5432/postgres?sslmode=require"
    SQLALCHEMY_DATABASE_URI: str
        
    # Supabase settings
    SUPABASE_URL: str = "https://zfcqnzovzfgdogwlkzsj.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmY3Fuem92emZnZG9nd2xrenNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MzQ4MTQsImV4cCI6MjA1NjUxMDgxNH0.-w8lZW-FwE_NCoX7XnqhmkzTvQRhppKxO5rCqcLUNwg"
    
    # OpenAI
    OPENAI_API_KEY: str = "your-openai-key-here"
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

    
