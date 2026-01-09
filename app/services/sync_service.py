from typing import List
from sqlalchemy.orm import Session
from app import crud, schemas

class SyncService:
    def reconcile_patients(self, db: Session, patients_in: List[schemas.PatientCreate], agent_id: int):
        """Traite un lot de patientes créées offline."""
        synced_count = 0
        errors = []

        for p_data in patients_in:
            # Vérifier si l'UUID existe déjà (doublon de synchro)
            existing = crud.patient.get_by_uuid(db, uuid=p_data.uuid)
            if existing:
                continue # Déjà synchronisé
            
            try:
                crud.patient.create_with_owner(db, obj_in=p_data, creator_id=agent_id)
                synced_count += 1
            except Exception as e:
                errors.append({"uuid": p_data.uuid, "error": str(e)})

        return {"synced": synced_count, "errors": errors}

sync_manager = SyncService()