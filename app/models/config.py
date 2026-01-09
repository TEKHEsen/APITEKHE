from sqlalchemy import Column, Integer, String, Float, JSON
from app.db.base_class import Base

class SystemConfig(Base):
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False) 
    value = Column(String, nullable=False)
    description = Column(String)
    category = Column(String) 