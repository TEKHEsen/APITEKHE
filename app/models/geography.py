from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from app.db.base_class import Base
import enum

class GeoLevel(str, enum.Enum):
    NATIONAL = "NATIONAL"
    REGIONAL = "REGIONAL"
    DISTRICT = "DISTRICT"
    POSTE = "POSTE"

class Geography(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    level = Column(Enum(GeoLevel), nullable=False)
    
    # Auto-relation pour la hiérarchie parent/enfant
    parent_id = Column(Integer, ForeignKey("geography.id"), nullable=True)
    
    # Relation pour remonter ou descendre dans l'arborescence
    children = relationship("Geography", backref=backref("parent", remote_side=[id]))
    
    # Relations avec les autres entités
    users = relationship("User", back_populates="geography")
    patients = relationship("Patient", back_populates="geography")