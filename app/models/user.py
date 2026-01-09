from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    
    phone = Column(String, unique=True, index=True, nullable=False)
    
    email = Column(String, unique=True, index=True, nullable=True)
    
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    

    role = Column(String, nullable=False)

    geography_id = Column(Integer, ForeignKey("geography.id"), nullable=True)
    geography = relationship("Geography", back_populates="users")
    
    
    consultations_faites = relationship("Consultation", back_populates="agent")
    

    
    def __repr__(self):
        return f"<User {self.full_name} - Role: {self.role} - Phone: {self.phone}>"