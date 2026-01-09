from typing import Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate # À créer/vérifier dans vos schémas

class CRUDUser:
    def get(self, db: Session, id: int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[User]:
        return db.query(User).filter(User.phone == phone).first()

    def authenticate(self, db: Session, *, phone: str, password: str) -> Optional[User]:
        """Vérifie les identifiants pour le login (Standard OAuth2 adapté au téléphone)."""
        user = self.get_by_phone(db, phone=phone)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Crée un utilisateur (National, Sage-femme, Patiente, etc.)."""
        db_obj = User(
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role,
            geography_id=obj_in.geography_id,
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_region(self, db: Session, *, geo_id: int) -> List[User]:
        return db.query(User).filter(User.geography_id == geo_id).all()

crud_user = CRUDUser()