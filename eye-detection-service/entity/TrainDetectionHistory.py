
# entity/TrainDetectionHistory.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .DetectEyeDataTrain import DetectEyeDataTrain

class TrainDetectionHistory(BaseModel):
    id: Optional[int] = None
    detectEyeDataTrain: DetectEyeDataTrain
    epochs: int
    batchSize: int
    imageSize: int
    learningRate: float
    timeTrain: Optional[datetime] = None
    
    def __init__(self, **data):
        super().__init__(**data)
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row, detect_eye_data_train=None):
        return cls(
            id=row["id"],
            detectEyeDataTrain=detect_eye_data_train,
            epochs=row["epochs"],
            batchSize=row["batchsize"],
            imageSize=row["imagesize"],
            learningRate=row["learningrate"],
            timeTrain=row["timetrain"]
        )
