from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime

# --- BASE PATIENT ---
class PatientBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    geography_id: Optional[int] = None
    preferred_language: Optional[str] = "fr"

# --- CRÉATION (Via Mobile Offline) ---
class PatientCreate(PatientBase):
    first_name: str
    last_name: str
    phone: str
    birth_date: date
    geography_id: int
    uuid: str = Field(..., description="UUID unique généré par l'application mobile")
    
    # Antécédents GHIF inclus dès l'enrôlement
    is_drepanocytaire_ss: bool = False
    nb_cesariennes: int = 0
    sterilite_prolongee: bool = False
    fausses_couches_repetition: bool = False
    grande_multiparite: bool = False
    taille_cm: Optional[float] = None

# --- MISE À JOUR ---
class PatientUpdate(PatientBase):
    is_enrolled_csu: Optional[bool] = None
    csu_status: Optional[str] = None # ACTIF, EN_ATTENTE, A_RENOUVELER
    csu_number: Optional[str] = None
    qr_code_hash: Optional[str] = None
    last_muac_cm: Optional[float] = None
    last_imc: Optional[float] = None
    date_renouvellement_csu: Optional[date] = None

# --- SORTIE API (Read) ---
class Patient(PatientBase):
    id: int
    uuid: str
    is_enrolled_csu: bool
    csu_status: str
    csu_number: Optional[str] = None
    qr_code_hash: Optional[str] = None
    
    # Données médicales & Nutrition
    is_drepanocytaire_ss: bool
    nb_cesariennes: int
    sterilite_prolongee: bool
    last_muac_cm: Optional[float] = None
    last_imc: Optional[float] = None
    
    created_at: datetime

    class Config:
        from_attributes = True 

# --- MODULE CSU ---
class CSUStatus(BaseModel):
    full_name: str
    is_active: bool
    csu_id: Optional[str]
    csu_status: str
    expiry_date: Optional[date]
    
class CSUEnrollmentCreate(BaseModel):
    patient_id: int
    structure_sante_id: Optional[int] = None
    attestation_communautaire: bool = False
    # Chemin vers la photo capturée par le mobile
    attestation_photo_path: Optional[str] = None

class CSUEnrollmentOut(BaseModel):
    status: str
    csu_number: str
    qr_code_hash: str
    message: str