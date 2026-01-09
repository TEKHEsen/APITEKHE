from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Consultation(Base):
    id = Column(Integer, primary_key=True, index=True)
    # UUID mobile pour éviter les collisions lors de la synchro
    uuid = Column(String, unique=True, index=True)
    
    patient_id = Column(Integer, ForeignKey("patient.id"))
    agent_id = Column(Integer, ForeignKey("user.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    type_visite = Column(String) # CPN1, CPN2, CPoN, etc.
    
    # Données biométriques (Corrections GHIF)
    poids = Column(Float)
    taille = Column(Float)
    hauteur_uterine = Column(Float)
    tension_arterielle = Column(String)
    
    # Facteurs de risque GHIF
    bassin_retreci = Column(Boolean, default=False)
    absence_maf = Column(Boolean, default=False)
    saignement = Column(Boolean, default=False)
    fievre = Column(Boolean, default=False)
    oedeme = Column(Boolean, default=False)
    
    # Résultat de l'IA/Moteur de règles
    risk_level = Column(String) # VERT, ORANGE, ROUGE
    risk_justification = Column(JSON) # Liste des drapeaux levés
    
    # Relations
    patient = relationship("Patient", back_populates="consultations")
    agent = relationship("User", back_populates="consultations_faites")