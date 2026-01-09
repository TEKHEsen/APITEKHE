from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    
    # Rôle hiérarchique : NATIONAL, REGIONAL, DISTRICT, POSTE
    role = Column(String, nullable=False)
    
    # Rattachement géographique
    geography_id = Column(Integer, ForeignKey("geography.id"))
    geography = relationship("Geography", back_populates="users")
    
    # Historique des actions
    consultations_faites = relationship("Consultation", back_populates="agent")