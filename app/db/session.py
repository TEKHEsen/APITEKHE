from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Création de l'engin SQLAlchemy
# pool_pre_ping=True permet de vérifier la validité de la connexion avant usage
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    pool_pre_ping=True
)

# Usine de sessions : chaque appel créera une nouvelle session de base de données
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)