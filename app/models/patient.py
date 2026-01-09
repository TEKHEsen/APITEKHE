from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- IDENTIFICATION & SYNC ---
    uuid = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    phone = Column(String, index=True)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- VOLET CSU (Couverture Sanitaire Universelle) ---
    is_enrolled_csu = Column(Boolean, default=False)
    csu_number = Column(String, unique=True, nullable=True)
    csu_status = Column(String, default="INACTIF") 
    csu_qr_hash = Column(String, unique=True, index=True, nullable=True)
    attestation_photo_path = Column(String, nullable=True)
    date_renouvellement_csu = Column(Date, nullable=True)

    # --- ANTÉCÉDENTS (Tableau A - GHIF) ---
    is_drepanocytaire_ss = Column(Boolean, default=False)
    nb_cesariennes = Column(Integer, default=0)
    sterilite_prolongee = Column(Boolean, default=False) 
    fausses_couches_repetition = Column(Boolean, default=False)
    grande_multiparite = Column(Boolean, default=False) 
    taille_cm = Column(Float, nullable=True) 


    last_poids_kg = Column(Float, nullable=True)
    last_muac_cm = Column(Float, nullable=True) 
    last_imc = Column(Float, nullable=True) 

    preferred_language = Column(String, default="fr") 
    whatsapp_enabled = Column(Boolean, default=True)


    geography_id = Column(Integer, ForeignKey("geography.id"), nullable=False)
    geography = relationship("Geography", back_populates="patients")
    
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} - CSU: {self.csu_status}>"