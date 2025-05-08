from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .EyeRecognitionSampleHistory import EyeRecognitionSampleHistory

class EyeRecognitionModel(BaseModel):
    id: Optional[int] = None
    modelLink: str = None
    eyeModelName: str  = None
    eyeRecognitionSampleTrain: list[EyeRecognitionSampleHistory]  = None
    accuracy: Optional[float] = None
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
   
    @classmethod
    def from_db_row(cls, row, sample_history=None):
        return cls(
            id=row["id"],
            modelLink=row["modellink"],
            eyeModelName=row["eyemodelname"],
            eyeRecognitionSampleTrain=sample_history,
            accuracy=row["accuracy"],
            isActive=row["isactive"],
            epochs=row["epochs"],
            learningRate=row["learningrate"],
            imageSize=row["imagesize"],
            batchSize=row["batchsize"],
            trainingTime=row["trainingtime"],
            mappingLabel=row["mappinglabel"],
            createDate=row["createdate"]
        )