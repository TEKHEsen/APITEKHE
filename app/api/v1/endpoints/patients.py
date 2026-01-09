from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Patient])
def read_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupère les patientes selon le périmètre géographique de l'utilisateur (Filtrage hiérarchique).
    """
    if current_user.role == "NATIONAL":
        patients = crud.patient.get_multi(db, skip=skip, limit=limit)
    elif current_user.role == "REGIONAL":
        patients = crud.patient.get_by_region(db, region_id=current_user.geography_id, skip=skip, limit=limit)
    elif current_user.role == "DISTRICT":
        patients = crud.patient.get_by_district(db, district_id=current_user.geography_id, skip=skip, limit=limit)
    else: 
        patients = crud.patient.get_by_poste(db, poste_id=current_user.geography_id, skip=skip, limit=limit)
        
    return patients

@router.post("/", response_model=schemas.Patient)
def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: schemas.PatientCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Créer une nouvelle patiente. 
    La patiente est automatiquement rattachée à la zone géographique de l'agent créateur si non spécifié.
    """
    if current_user.role != "NATIONAL" and patient_in.geography_id != current_user.geography_id:
        patient_in.geography_id = current_user.geography_id

    patient = crud.patient.create_with_owner(
        db, obj_in=patient_in, creator_id=current_user.id
    )
    return patient

@router.get("/{id}", response_model=schemas.Patient)
def read_patient(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Récupérer une patiente par son ID avec vérification stricte des droits géographiques.
    """
    patient = crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Patiente non trouvée"
        )
    

    if current_user.role != "NATIONAL":
        is_authorized = crud.geography.is_subzone_or_same(
            db, 
            parent_id=current_user.geography_id, 
            child_id=patient.geography_id
        )
        if not is_authorized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé : Cette patiente ne dépend pas de votre zone géographique."
            )
    
    return patient