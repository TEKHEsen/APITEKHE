from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.services.config_service import config_manager
from app.models.user import User

from app.utils.audit import log_action
from app.models.config import SystemConfig

router = APIRouter()

@router.get("/utilisateurs", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.CheckerRole(["NATIONAL", "REGIONAL"])),
) -> Any:
    """
    Liste les utilisateurs sous la responsabilité du gestionnaire connecté.
    Un gestionnaire Régional ne verra que les agents de sa région.
    """
    return crud.user.get_multi_by_scope(
        db, scope_user=current_user, skip=skip, limit=limit
    )

@router.post("/utilisateurs", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.CheckerRole(["NATIONAL", "REGIONAL", "DISTRICT"])),
) -> Any:
    """
    Créer un utilisateur (ex: District crée une SFE ou un ICP).
    Vérifie que la zone géo du nouvel utilisateur est incluse dans celle du créateur.
    """
    if not crud.geography.is_subzone(db, parent_id=current_user.geography_id, child_id=user_in.geography_id):
        raise HTTPException(status_code=403, detail="Zone géographique hors de votre contrôle")
    
    return crud.user.create(db, obj_in=user_in)

@router.get("/geographies", response_model=List[schemas.Geography])
def get_zones(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Récupère l'arborescence géographique accessible à l'utilisateur."""
    return crud.geography.get_children(db, parent_id=current_user.geography_id)




@router.put("/thresholds/{key}")
def update_clinical_threshold(
    key: str,
    value: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.role != "NATIONAL":
        raise HTTPException(status_code=403, detail="Seul le Gestionnaire National peut modifier les seuils")
    
    # 1. On récupère l'ancienne valeur pour l'audit
    old_config = db.query(SystemConfig).filter(SystemConfig.key == key).first()
    old_value = old_config.value if old_config else "Inconnu"

    # 2. Mise à jour via le service
    updated = config_manager.update_config(db, key, value)
    if not updated:
        raise HTTPException(status_code=404, detail="Paramètre non trouvé")
    
    # 3. ENREGISTREMENT DU LOG D'AUDIT
    log_action(
        db,
        user_id=current_user.id,
        action="UPDATE_THRESHOLD",
        resource="SystemConfig",
        resource_id=key,
        details={
            "old_value": old_value,
            "new_value": value,
            "parameter": key
        }
    )
    
    return {"message": f"Le paramètre {key} a été mis à jour à {value}"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.init_db import init_db

router = APIRouter()
@router.get("/setup-database-initial-tekhe")
def setup_db(db: Session = Depends(deps.get_db)):
    try:
        init_db(db)
        return {"status": "success", "message": "Tables creees et Admin initialise"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
from app.schemas.audit import AuditLogOut
from app.models.audit import AuditLog

@router.get("/logs", response_model=list[AuditLogOut])
def get_audit_logs(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    limit: int = 100
):
    if current_user.role != "NATIONAL":
        raise HTTPException(status_code=403, detail="Accès réservé au niveau National")
    
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()