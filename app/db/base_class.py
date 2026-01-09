from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str
    
    # Génère automatiquement le nom de la table à partir du nom de la classe en minuscules
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Vous pouvez ajouter ici des colonnes communes à toutes les tables si nécessaire
    # Exemple : created_at, updated_at