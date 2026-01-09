from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils.audit import log_action  # Import de la fonction utilitaire

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    request: Request, # Ajouté pour capturer l'IP si nécessaire
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Connexion compatible OAuth2. 
    Le champ 'username' du formulaire doit contenir le NUMÉRO DE TÉLÉPHONE.
    """
    # Tentative d'authentification
    user = crud.user.authenticate(
        db, phone=form_data.username, password=form_data.password
    )
    
    if not user:
        # LOG : Échec de connexion (important pour détecter les attaques par brute force)
        # Comme on n'a pas de user_id, on met 0 ou None
        log_action(
            db, 
            user_id=None, 
            action="LOGIN_FAILED", 
            resource="AUTH", 
            details={"phone_attempted": form_data.username, "ip": request.client.host}
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Numéro de téléphone ou mot de passe incorrect"
        )
        
    if not user.is_active:
        # LOG : Tentative sur compte inactif
        log_action(db, user_id=user.id, action="LOGIN_INACTIVE", resource="AUTH")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Compte utilisateur inactif"
        )
    
    # LOG : Connexion réussie
    log_action(
        db, 
        user_id=user.id, 
        action="LOGIN_SUCCESS", 
        resource="AUTH",
        details={"role": user.role}
    )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/test-token", response_model=schemas.UserOut)
def test_token(
    db: Session = Depends(deps.get_db), # Ajouté pour les logs
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    """
    Vérifie si le token est valide et renvoie les infos de l'utilisateur actuel.
    """
    # LOG : Vérification de token (optionnel, peut être verbeux)
    log_action(db, user_id=current_user.id, action="TOKEN_VERIFY", resource="AUTH")
    
    return current_user