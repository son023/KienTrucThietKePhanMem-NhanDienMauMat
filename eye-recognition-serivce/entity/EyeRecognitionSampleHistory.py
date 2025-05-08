from pydantic import BaseModel
from .EyeRecognitionSample import EyeRecognitionSample

class EyeRecognitionSampleHistory(BaseModel):
    id: int = None
    eyeRecognitionSample: EyeRecognitionSample
    notes: str = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row, samples=None):
        return cls(
            id=row["id"],
            notes=row["notes"],
            eyeRecognitionSample=samples
        )
    
