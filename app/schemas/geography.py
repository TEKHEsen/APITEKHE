from typing import List, Optional
from pydantic import BaseModel

class GeographyBase(BaseModel):
    name: str
    level: str
    parent_id: Optional[int] = None

class GeographyCreate(GeographyBase):
    pass

class Geography(GeographyBase):
    id: int

    class Config:
        from_attributes = True

class GeographyWithChildren(Geography):
    children: List['Geography'] = []