from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Consultation)
def create_visite(
    *,
    db: Session = Depends(deps.get_db),
    visite_in: schemas.ConsultationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Créer une consultation (CPN/CPoN) avec calcul automatique du risque."""
    return crud.consultation.create_with_analysis(
        db, obj_in=visite_in, agent_id=current_user.id
    )

@router.post("/batch", response_model=List[schemas.Consultation])
def create_visites_batch(
    *,
    db: Session = Depends(deps.get_db),
    visites_in: List[schemas.ConsultationCreate],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Endpoint pour la synchronisation offline (upload groupé)."""
    return crud.consultation.create_batch(db, obj_list=visites_in, agent_id=current_user.id)

@router.get("/patient/{patient_id}", response_model=List[schemas.Consultation])
def read_visites_by_patient(
    patient_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Historique des visites d'une patiente."""
    return crud.consultation.get_by_patient(db, patient_id=patient_id)