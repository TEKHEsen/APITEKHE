from enum import Enum

class RiskLevel(str, Enum):
    GREEN = "VERT"
    ORANGE = "ORANGE"
    RED = "ROUGE"

# --- RÔLES UTILISATEURS (Fixes) ---
ROLES = {
    "NATIONAL": "Gestionnaire National (Contrôle total)",
    "REGIONAL": "Direction Régionale de la Santé",
    "DISTRICT": "District Sanitaire",
    "POSTE": "Prestataire de Terrain (Sage-femme, ICP, Badiénou Gox)"
}

# --- VALEURS PAR DÉFAUT (Initialisation) ---
DEFAULT_CONFIGS = {
    "AGE_MIN_CRITIQUE": "15",
    "AGE_MAX_CRITIQUE": "35",
    "TAILLE_MIN_CM": "152",
    "HU_MAX_THRESHOLD": "34",
    "SYNC_BATCH_SIZE": "50"
}