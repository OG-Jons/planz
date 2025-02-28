from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "fastapi"
    POSTGRES_PASSWORD: str = "secret"
    POSTGRES_DB: str = "plantsdb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings()