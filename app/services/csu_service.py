import hashlib
import uuid
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientUpdate
from typing import Any

class CSUService:
    def generate_qr_hash(self, patient_uuid: str) -> str:
        """Génère un hash unique pour le QR Code CSU."""
        salt = "TEKHE_SENEGAL_2025"
        return hashlib.sha256(f"{patient_uuid}{salt}".encode()).hexdigest()

    def process_enrollment(self, db: Session, patient: Patient, data: Any) -> Any:
        """Finalise l'enrôlement et génère les identifiants CSU."""
        # Simulation d'appel API vers l'Agence Nationale CSU ici
        csu_id = f"SN-CSU-{uuid.uuid4().hex[:8].upper()}"
        qr_hash = self.generate_qr_hash(patient.uuid)

        patient.is_enrolled_csu = True
        patient.csu_number = csu_id
        patient.qr_code_hash = qr_hash
        
        db.add(patient)
        db.commit()
        db.refresh(patient)
        
        return {
            "status": "success",
            "csu_number": csu_id,
            "qr_code_hash": qr_hash,
            "message": "Enrôlement réussi"
        }

csu_manager = CSUService()