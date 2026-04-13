from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_URL: str = "postgresql+asyncpg://user:password@localhost:5432/cqrs_db"

    # MongoDB
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "cqrs_db"

    class Config:
        env_file = ".env"


settings = Settings()
