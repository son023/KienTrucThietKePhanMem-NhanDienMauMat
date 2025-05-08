from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EyeRecognitionSample(BaseModel):
    id: Optional[int] = None
    memberId: int
    eyeImageLink: str
    label: Optional[int] = None
    isActive: bool = True
    captureDate: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row["id"],
            memberId=row["memberid"],
            eyeImageLink=row["eyeimagelink"],
            label=row["label"],
            isActive=row["isactive"], 
            captureDate=row["capturedate"]
        )