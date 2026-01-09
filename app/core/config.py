import pathlib
from typing import List, Union, Optional, Any
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

# Chemin racine du projet
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TEKHE API"
    
    # Sécurité & JWT
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours
    
    # Configuration du premier Administrateur
    FIRST_SUPERUSER: str = "admin@tekhe.sn"
    FIRST_SUPERUSER_PASSWORD: str = "TekheSenegal2026!"
    
    # --- BASE DE DONNÉES ---
    # En production (ex: Render/Railway), DATABASE_URL est souvent fournie directement.
    # En local, on utilise les variables séparées.
    DATABASE_URL: Optional[str] = None 
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "aipenpass123"
    POSTGRES_DB: str = "tekhe_db"
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        
        db_url = info.data.get("DATABASE_URL")
        if db_url:
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return db_url
            
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        server = info.data.get("POSTGRES_SERVER")
        db = info.data.get("POSTGRES_DB")
        
        return f"postgresql://{user}:{password}@{server}/{db}"

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return []

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore" 
    }

settings = Settings()