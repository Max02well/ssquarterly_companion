from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):

    APP_NAME: str = "Quarterly Companion"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str
    
    DB_PASSWORD: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: str
    
    OLLAMA_API_KEY: str | None = None
    OLLAMA_BASE_URL: str | None = None
    OLLAMA_MODEL: str | None = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    OPENAI_API_KEY: str | None = None

    CHROMA_PATH: str = "data/chromadb"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
    # @property
    # def DATABASE_URL_encoded(self) -> str:
    #     """Return DATABASE_URL with password URL-encoded"""
    #     if self.DATABASE_URL:
    #         # Parse the URL and encode the password
    #         # This is a simple approach - for production use a proper URL parser
    #         parts = self.DATABASE_URL.split('://')
    #         if len(parts) == 2:
    #             prefix, rest = parts
    #             # Extract user:password@host:port/database
    #             if '@' in rest:
    #                 auth, host_db = rest.split('@', 1)
    #                 if ':' in auth:
    #                     user, password = auth.split(':', 1)
    #                     encoded_password = quote_plus(password)
    #                     return f"{prefix}://{user}:{encoded_password}@{host_db}"
    #     return self.DATABASE_URL


settings = Settings()