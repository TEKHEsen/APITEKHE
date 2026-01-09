from typing import Optional
from pydantic import BaseModel, EmailStr

# Propriétés communes
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    role: Optional[str] = None
    geography_id: Optional[int] = None

# Propriétés à recevoir via l'API lors de la création
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Propriétés à retourner via l'API
class User(UserBase):
    id: int

    class Config:
        from_attributes = True