# app/crud/__init__.py

# On importe l'instance 'patient' depuis le fichier crud_patient.py
from .crud_patient import patient
# On crée un alias 'crud_patient' pour satisfaire les imports qui utilisent ce nom
crud_patient = patient

# Même logique pour les autres modules si ils existent
try:
    from .crud_visite import crud_consultation
    consultation = crud_consultation
except ImportError:
    pass

try:
    from .crud_user import crud_user
    user = crud_user
except ImportError:
    pass