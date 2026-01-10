from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.schemas.risk import RiskInputSchema, RiskAnalysisOut
from app.core.constants import RiskLevel
from app.services.config_service import config_manager
from app.models.user import User

class RiskService:
    def evaluate_risk(self, db: Session, data: RiskInputSchema) -> RiskAnalysisOut:
        flags = []
        recommendations = []
        level = RiskLevel.GREEN

        # Récupération des seuils dynamiques via le National Config
        age_min = config_manager.get_value(db, "AGE_MIN_CRITIQUE") or 18
        age_max = config_manager.get_value(db, "AGE_MAX_CRITIQUE") or 35
        hu_max = config_manager.get_value(db, "HU_MAX_THRESHOLD") or 34

        # --- LOGIQUE GHIF : FACTEURS MAJEURS (ROUGE) ---
        if data.bassin_retreci:
            level = RiskLevel.RED
            flags.append("Anomalie du bassin (bassin rétréci)")
            recommendations.append("Référence immédiate vers centre SONU")

        if data.saignement:
            level = RiskLevel.RED
            flags.append("Saignements / Hémorragies")
            recommendations.append("URGENCE : Transfert immédiat vers CHR")

        if data.absence_maf:
            level = RiskLevel.RED
            flags.append("Absence de Mouvements Actifs Fœtaux (MAF)")
            recommendations.append("Vérification immédiate du rythme cardiaque fœtal")

        # --- LOGIQUE GHIF : FACTEURS MODÉRÉS (ORANGE) ---
        if data.age < age_min or data.age > age_max:
            if level != RiskLevel.RED: level = RiskLevel.ORANGE
            flags.append(f"Âge critique ({data.age} ans)")
            recommendations.append("Suivi prénatal renforcé")

        if data.fievre:
            if level != RiskLevel.RED: level = RiskLevel.ORANGE
            flags.append("Fièvre détectée")

        if data.oedeme:
            if level != RiskLevel.RED: level = RiskLevel.ORANGE
            flags.append("Œdèmes des membres/visage")

        if data.hauteur_uterine > hu_max:
            if level != RiskLevel.RED: level = RiskLevel.ORANGE
            flags.append(f"Hauteur Utérine excessive (> {hu_max}cm)")

        if not flags:
            recommendations.append("Continuer le suivi prénatal standard.")

        return RiskAnalysisOut(
            risk_level=level,
            justification=flags,
            recommendations=recommendations
        )

    def get_stats_by_user_scope(self, current_user: User) -> Dict[str, Any]:
        """
        Méthode manquante qui causait le crash du dashboard.
        Retourne les statistiques de risques basées sur le rôle de l'utilisateur.
        """
        # Note: En production, vous feriez des requêtes SQL réelles ici.
        # Voici une structure de retour compatible avec votre Dashboard.
        return {
            "total_evaluations": 0,
            "distribution": {
                "RED": 0,
                "ORANGE": 0,
                "GREEN": 0
            },
            "scope": current_user.role,
            "region": "National"
        }

# Instance unique pour l'application
risk_service = RiskService()