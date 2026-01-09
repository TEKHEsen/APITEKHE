import logging
from typing import Any, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog

# Configuration du logger pour voir les actions dans la console de Render
logger = logging.getLogger("tekhe_audit")

def log_action(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    details: Optional[Any] = None
) -> None:
    """
    Enregistre une action utilisateur dans la table audit_log et dans les logs système.
    """
    try:
        # 1. Création de l'entrée en base de données
        new_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details
        )
        db.add(new_log)
        db.commit()
        
        # 2. Doublage dans les logs console de Render (pour debug rapide)
        msg = f"AUDIT: User {user_id} | Action: {action} | Resource: {resource} ({resource_id})"
        logger.info(msg)
        
    except Exception as e:
        # On ne bloque pas l'application si le log échoue
        db.rollback()
        logger.error(f"Erreur lors de l'enregistrement du log d'audit : {str(e)}")