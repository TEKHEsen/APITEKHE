from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Connexion compatible OAuth2. 
    Le champ 'username' du formulaire doit contenir le NUMÉRO DE TÉLÉPHONE.
    """
    # On authentifie via le numéro de téléphone
    user = crud.user.authenticate(
        db, phone=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Numéro de téléphone ou mot de passe incorrect"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Compte utilisateur inactif"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # On génère le token avec l'ID de l'utilisateur
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/test-token", response_model=schemas.UserOut) # Utilisation de UserOut pour ne pas renvoyer le pass
def test_token(current_user: schemas.User = Depends(deps.get_current_user)) -> Any:
    """
    Vérifie si le token est valide et renvoie les infos de l'utilisateur actuel.
    """
    return current_user