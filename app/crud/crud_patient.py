from typing import List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

class CRUDPatient:
    # --- LECTURE ---

    def get(self, db: Session, id: int) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.id == id).first()

    def get_by_uuid(self, db: Session, uuid: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.uuid == uuid).first()

    def get_by_qr_hash(self, db: Session, qr_hash: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.csu_qr_hash == qr_hash).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Patient]:
        return db.query(Patient).order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_geography(self, db: Session, *, geo_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
        """
        Récupère les patientes pour une zone spécifique. 
        """
        return db.query(Patient).filter(Patient.geography_id == geo_id).offset(skip).limit(limit).all()

    def get_by_region(self, db: Session, *, region_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
        return self.get_by_geography(db, geo_id=region_id, skip=skip, limit=limit)

    def get_by_district(self, db: Session, *, district_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
        return self.get_by_geography(db, geo_id=district_id, skip=skip, limit=limit)

    def get_by_poste(self, db: Session, *, poste_id: int, skip: int = 0, limit: int = 100) -> List[Patient]:
        return self.get_by_geography(db, geo_id=poste_id, skip=skip, limit=limit)

    # --- ACTIONS ---

    def create_with_owner(self, db: Session, *, obj_in: PatientCreate, creator_id: int) -> Patient:
        obj_in_data = obj_in.model_dump()
        db_obj = Patient(
            **obj_in_data,
            creator_id=creator_id,
            csu_status="INACTIF" 
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Patient, obj_in: Union[PatientUpdate, Dict[str, Any]]
    ) -> Patient:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

patient = CRUDPatient()