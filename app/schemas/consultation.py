from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ConsultationBase(BaseModel):
    patient_id: int
    type_visite: str  # CPN1, CPN2, etc.
    poids: float
    taille: float
    hauteur_uterine: float
    bassin_retreci: bool = False
    fievre: bool = False
    saignement: bool = False
    oedeme: bool = False
    absence_maf: bool = False

class ConsultationCreate(ConsultationBase):
    uuid: str  # Généré par le mobile pour le offline
    age: int   # Pour le moteur de risque

class Consultation(ConsultationBase):
    id: int
    uuid: str
    agent_id: int
    created_at: datetime
    risk_level: str
    risk_justification: List[str]

    class Config:
        from_attributes = True