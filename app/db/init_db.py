from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.models.config import SystemConfig
from app.models.geography import Geography, GeoLevel
from app.core.constants import DEFAULT_CONFIGS
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # 1. Création de la Géographie Racine (Sénégal)
    national_zone = db.query(Geography).filter(Geography.level == GeoLevel.NATIONAL).first()
    if not national_zone:
        national_zone = Geography(
            name="Sénégal",
            level=GeoLevel.NATIONAL,
            parent_id=None
        )
        db.add(national_zone)
        db.commit()
        db.refresh(national_zone)
        print("✅ Zone Nationale (Sénégal) créée.")

    # 2. Création du premier compte Gestionnaire National
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Administrateur National TEKHE",
            role="NATIONAL",
            geography_id=national_zone.id
        )
        # Note: Assurez-vous d'avoir crud.user.create implémenté
        from app.models.user import User
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role=user_in.role,
            geography_id=user_in.geography_id,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        print(f"✅ Premier utilisateur créé : {settings.FIRST_SUPERUSER}")

    # 3. Initialisation des seuils cliniques (Configuration Système)
    for key, value in DEFAULT_CONFIGS.items():
        config_exists = db.query(SystemConfig).filter(SystemConfig.key == key).first()
        if not config_exists:
            new_config = SystemConfig(
                key=key,
                value=value,
                description=f"Seuil par défaut pour {key}",
                category="CLINIQUE" if "AGE" in key or "HU" in key else "SYSTEM"
            )
            db.add(new_config)
    
    db.commit()
    print("✅ Seuils cliniques par défaut insérés en base de données.")

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    init_db(db)