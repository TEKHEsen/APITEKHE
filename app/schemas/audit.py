from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource: str
    resource_id: Optional[str]
    details: Optional[Any]
    timestamp: datetime

    class Config:
        from_attributes = True