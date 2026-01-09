from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from app.db.base_class import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id")) # Qui a fait l'action
    action = Column(String) # Ex: "LOGIN", "UPDATE_SEUIL", "CREATE_PATIENT"
    resource = Column(String) # Ex: "Patient", "SystemConfig"
    resource_id = Column(String, nullable=True) # ID de l'élément modifié
    details = Column(JSON) # Les changements (Ancienne valeur vs Nouvelle)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String, nullable=True)