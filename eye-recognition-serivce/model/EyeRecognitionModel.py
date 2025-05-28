from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .EyeRecognitionSampleHistory import EyeRecognitionSampleHistory
import uuid

class EyeRecognitionModel(BaseModel):
    id: Optional[str] = None
    modelLink: str = None
    eyeModelName: str  = None
    eyeRecognitionSampleHistory: list[EyeRecognitionSampleHistory]  = None
    accuracy: Optional[float] = None
    f1Score: Optional[float] = None
    precision: Optional[float] = None
    isActive: bool = True
    epochs: Optional[int] = None
    learningRate: Optional[float] = None
    imageSize: Optional[int] = None
    batchSize: Optional[int] = None
    mappingLabel: Optional[str] = None
    trainingTime:Optional[int] = None
    createDate: Optional[datetime] = None
   
    class Config:
        from_attributes = True