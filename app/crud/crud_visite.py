from typing import List
from sqlalchemy.orm import Session
from app.models.consultation import Consultation
from app.schemas.risk import RiskInputSchema
from app.services.risk_engine import risk_service
from app import schemas

class CRUDConsultation:
    def create_with_analysis(self, db: Session, *, obj_in: schemas.ConsultationCreate, agent_id: int) -> Consultation:
        # 1. Préparer les données pour le moteur de risque IA
        risk_input = RiskInputSchema(
            age=obj_in.age, # L'âge doit être calculé ou passé en paramètre
            poids=obj_in.poids,
            taille=obj_in.taille,
            hauteur_uterine=obj_in.hauteur_uterine,
            bassin_retreci=obj_in.bassin_retreci,
            fievre=obj_in.fievre,
            saignement=obj_in.saignement,
            oedeme=obj_in.oedeme,
            absence_maf=obj_in.absence_maf
        )
        
        # 2. Exécuter l'analyse de risque
        analysis = risk_service.evaluate_risk(db, data=risk_input)
        
        # 3. Créer l'objet en base
        db_obj = Consultation(
            uuid=obj_in.uuid,
            patient_id=obj_in.patient_id,
            agent_id=agent_id,
            type_visite=obj_in.type_visite,
            poids=obj_in.poids,
            taille=obj_in.taille,
            hauteur_uterine=obj_in.hauteur_uterine,
            bassin_retreci=obj_in.bassin_retreci,
            risk_level=analysis.risk_level,
            risk_justification=analysis.justification
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_patient(self, db: Session, *, patient_id: int) -> List[Consultation]:
        return db.query(Consultation).filter(Consultation.patient_id == patient_id).all()

    def create_batch(self, db: Session, *, obj_list: List[schemas.ConsultationCreate], agent_id: int) -> List[Consultation]:
        """Utilisé pour la synchronisation de masse depuis le mobile."""
        results = []
        for obj_in in obj_list:
            res = self.create_with_analysis(db, obj_in=obj_in, agent_id=agent_id)
            results.append(res)
        return results

crud_consultation = CRUDConsultation()