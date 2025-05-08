# entity/DetectEyeData.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DetectEyeData(BaseModel):
    id: Optional[int] = None
    imageLink: str
    labelLink: str
    
    def __init__(self, **data):
        super().__init__(**data)
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row["id"],
            imageLink=row["imagelink"],
            labelLink=row["labellink"]
        )