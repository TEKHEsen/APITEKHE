from enum import Enum

class RiskLevel(str, Enum):
    GREEN = "VERT"
    ORANGE = "ORANGE"
    RED = "ROUGE"


ROLES = {
    "NATIONAL": "Gestionnaire National (Controle total)",
    "REGIONAL": "Direction Regionale de la Sante",
    "DISTRICT": "District Sanitaire",
    "POSTE": "Prestataire de Terrain (Sage-femme, ICP, Badienou Gox)"
}

DEFAULT_CONFIGS = {
    "AGE_MIN_CRITIQUE": "15",
    "AGE_MAX_CRITIQUE": "35",
    "TAILLE_MIN_CM": "152",
    "HU_MAX_THRESHOLD": "34",
    "SYNC_BATCH_SIZE": "50"
}