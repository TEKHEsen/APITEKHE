from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.services.csu_service import csu_manager

router = APIRouter()

@router.post("/enroler", response_model=schemas.CSUEnrollmentOut)
def enroler_csu(
    *,
    db: Session = Depends(deps.get_db),
    enrol_in: schemas.CSUEnrollmentCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Enrôle une patiente à la CSU et génère la preuve numérique (QR Code).
    Accepte les attestations communautaires si pas de CNI.
    """
    patient = crud.patient.get(db, id=enrol_in.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    
    return csu_manager.process_enrollment(db, patient=patient, data=enrol_in)

@router.get("/verifier/{qr_hash}", response_model=schemas.CSUStatus)
def verifier_statut_csu(
    qr_hash: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """Endpoint utilisé par les structures SONU pour valider la prise en charge."""
    status = crud.patient.get_by_qr_hash(db, qr_hash=qr_hash)
    if not status:
        raise HTTPException(status_code=404, detail="Preuve CSU invalide")
    return status