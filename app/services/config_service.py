from sqlalchemy.orm import Session
from app.models.config import SystemConfig
from app.core.constants import DEFAULT_CONFIGS

class ConfigService:
    def get_value(self, db: Session, key: str) -> float:
        db_config = db.query(SystemConfig).filter(SystemConfig.key == key).first()
        if db_config:
            return float(db_config.value)
        return float(DEFAULT_CONFIGS.get(key, 0))

    def update_config(self, db: Session, key: str, new_value: str):
        db_config = db.query(SystemConfig).filter(SystemConfig.key == key).first()
        if db_config:
            db_config.value = new_value
            db.commit()
            return db_config
        return None

config_manager = ConfigService()