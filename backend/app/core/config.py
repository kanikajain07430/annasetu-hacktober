import os

class Settings:
    PROJECT_NAME: str = "AnnaSetu Platform API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DB_PATH: str = os.path.join(BASE_DIR, "annasetu.db")
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "annasetu-super-secure-production-secret-key-change-in-env")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

settings = Settings()
