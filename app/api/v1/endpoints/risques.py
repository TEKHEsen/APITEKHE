from typing import Any
from fastapi import APIRouter, Depends
from app import schemas
from app.api import deps
from app.services.risk_engine import risk_service

router = APIRouter()

@router.post("/analyser", response_model=schemas.RiskAnalysisOut)
def analyser_risque(
    *,
    data: schemas.RiskInputSchema,
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Simuler une analyse de risque sans enregistrement en base.
    Inclut les facteurs GHIF (Bassin, Âge, HU).
    """
    analysis = risk_service.evaluate_risk(data)
    return analysis

@router.get("/statistiques-regionales", response_model=schemas.RiskStats)
def get_risk_stats(
    current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """Affiche la répartition des sémaphores (Vert/Orange/Rouge) pour le Dashboard."""
    # Filtrage géographique appliqué via le service
    return risk_service.get_stats_by_user_scope(current_user)