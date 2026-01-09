from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.geography import Geography
from app.models.patient import Patient # Assurez-vous que ce modèle existe

class CRUDStats:
    def get_national_summary(self, db: Session):
        # 1. Distribution des risques
        risk_counts = db.query(
            Patient.last_risk_level, 
            func.count(Patient.id)
        ).group_by(Patient.last_risk_level).all()
        
        # 2. Total patientes
        total = db.query(func.count(Patient.id)).scalar()
        
        return {
            "total_patients": total,
            "risk_distribution": dict(risk_counts),
            "total_alerts_active": db.query(func.count(Patient.id)).filter(Patient.last_risk_level == "ROUGE").scalar()
        }

crud_stats = CRUDStats()