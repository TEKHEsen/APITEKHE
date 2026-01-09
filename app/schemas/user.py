from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# --- PROPRIÉTÉS COMMUNES ---
class UserBase(BaseModel):
    phone: Optional[str] = Field(None, description="Numéro de téléphone servant d'identifiant")
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = None # 'NATIONAL', 'REGION', 'DISTRICT', 'SAGE_FEMME', 'BADIENOU_GOX', 'PATIENTE'
    geography_id: Optional[int] = None

# --- CRÉATION ---
class UserCreate(UserBase):
    phone: str = Field(..., description="Le numéro de téléphone est obligatoire pour créer un compte")
    password: str = Field(..., min_length=4, description="Mot de passe ou Code PIN")
    role: str

# --- MISE À JOUR ---
class UserUpdate(UserBase):
    password: Optional[str] = None

# --- MODÈLE DE BASE POUR LA LECTURE ---
class User(UserBase):
    id: int
    phone: str
    role: str

    class Config:
        from_attributes = True 

class UserOut(User):
    """
    Schéma utilisé pour renvoyer les données utilisateur sans informations sensibles.
    Il hérite de User qui contient déjà id, phone, role, full_name, etc.
    """
    pass