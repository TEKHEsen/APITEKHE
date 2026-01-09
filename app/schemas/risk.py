from typing import List, Optional
from pydantic import BaseModel
from app.core.constants import RiskLevel

class RiskInputSchema(BaseModel):
    age: int
    poids: float
    taille: float
    hauteur_uterine: float
    bassin_retreci: bool = False
    fievre: bool = False
    saignement: bool = False
    oedeme: bool = False
    absence_maf: bool = False

class RiskAnalysisOut(BaseModel):
    risk_level: RiskLevel
    justification: List[str]
    recommendations: List[str]

class RiskStats(BaseModel):
    total_patients: int
    red_count: int
    orange_count: int
    green_count: int