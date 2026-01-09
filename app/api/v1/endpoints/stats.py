from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.schemas.stats import NationalStats
from app.crud.crud_stats import crud_stats

router = APIRouter()

@router.get("/national", response_model=NationalStats)
def read_national_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    # Sécurité : Vérification du rôle
    if current_user.role != "NATIONAL":
        raise HTTPException(
            status_code=403, 
            detail="Seul le Gestionnaire National peut accéder à ces données"
        )
    
    return crud_stats.get_national_summary(db)