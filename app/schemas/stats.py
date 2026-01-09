from pydantic import BaseModel
from typing import Dict, List

class NationalStats(BaseModel):
    total_patients: int
    risk_distribution: Dict[str, int] 
    total_alerts_active: int
    enrolment_by_region: Dict[str, int] 