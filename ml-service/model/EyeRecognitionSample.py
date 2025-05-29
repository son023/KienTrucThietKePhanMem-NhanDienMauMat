from pydantic import BaseModel, field_validator
from typing import Optional, Union, List
from datetime import datetime
from .Member import Member
import uuid

class EyeRecognitionSample(BaseModel):
    id: Optional[str] = None
    eyeImageLink: str
    label: Optional[str] = None
    isActive: bool = True
    captureDate: Optional[Union[str, List[int]]] = None  # Accept both string and array
    member: Optional[Member] = None  # Nested member object (optional)
    
    @field_validator('captureDate')
    def validate_capture_date(cls, v):
        if v is None:
            return None
        if isinstance(v, list):
            # Convert array format [2025,5,28,2,7,49,687351000] to string
            if len(v) >= 6:
                year, month, day, hour, minute, second = v[:6]
                return f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"
        return str(v)
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row["id"],
            eyeImageLink=row["eyeimagelink"],
            label=row["label"],
            isActive=row["isactive"], 
            captureDate=row["capturedate"]
        )