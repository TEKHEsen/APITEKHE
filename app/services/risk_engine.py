from typing import List
from sqlalchemy.orm import Session
from app.schemas.risk import RiskInputSchema, RiskAnalysisOut
from app.core.constants import RiskLevel
from app.services.config_service import config_manager

class RiskService:
    def evaluate_risk(self, db: Session, data: RiskInputSchema) -> RiskAnalysisOut:
        flags = []
        recommendations = []
        level = RiskLevel.GREEN

        # Récupération des seuils dynamiques via le National Config
        age_min = config_manager.get_value(db, "AGE_MIN_CRITIQUE")
        age_max = config_manager.get_value(db, "AGE_MAX_CRITIQUE")
        hu_max = config_manager.get_value(db, "HU_MAX_THRESHOLD")

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

risk_service = RiskService()