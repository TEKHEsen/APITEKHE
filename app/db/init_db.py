from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings
from app.models.config import SystemConfig
from app.models.geography import Geography, GeoLevel
from app.core.constants import DEFAULT_CONFIGS
from app.core.security import get_password_hash
from app.models.user import User

def init_db(db: Session) -> None:
    # 1. Zone nationale
    national_zone = db.query(Geography).filter(Geography.level == GeoLevel.NATIONAL).first()
    if not national_zone:
        national_zone = Geography(
            name="Senegal", 
            level=GeoLevel.NATIONAL,
            parent_id=None
        )
        db.add(national_zone)
        db.commit()
        db.refresh(national_zone)
        print("Zone Nationale creee.")

    # 2. Compte Admin
    admin_phone = "774532238"
    user = db.query(User).filter(User.phone == admin_phone).first()
    
    if not user:
        db_user = User(
            phone=admin_phone,
            email="papaseydou.wane@unchk.edu.sn",
            full_name="Papa Seydou WANE",
            hashed_password=get_password_hash("Qqmkl@8345"),
            role="NATIONAL",
            geography_id=national_zone.id,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        print(f"Compte Admin cree: {admin_phone}")
    else:
        print(f"L'admin {admin_phone} existe deja.")

    # 3. Seuils cliniques
    print("Initialisation des seuils...")
    for key, value in DEFAULT_CONFIGS.items():
        config_exists = db.query(SystemConfig).filter(SystemConfig.key == key).first()
        if not config_exists:
            new_config = SystemConfig(
                key=key,
                value=str(value),
                description=f"Seuil pour {key}",
                category="CLINIQUE" if any(x in key for x in ["AGE", "HU", "IMC", "POIDS"]) else "SYSTEM"
            )
            db.add(new_config)
    
    db.commit()
    print("Configuration terminee.")

if __name__ == "__main__":
    from app.db.session import SessionLocal
    print("Demarrage de l'initialisation...")
    db = SessionLocal()
    try:
        init_db(db)
        print("Fini avec succes.")
    except Exception as e:
        print(f"Erreur fatale : {str(e)}")
    finally:
        db.close()