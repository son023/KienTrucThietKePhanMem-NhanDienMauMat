# entity/EyeDetectionModel.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .TrainDetectionHistory import TrainDetectionHistory

class EyeDetectionModel(BaseModel):
    id: Optional[int] = None
    modelName: str
    trainDetectionHistory: Optional[List[TrainDetectionHistory]] = []
    mapMetrix: float
    isActive: bool = True
    modelLink: str
    createDate: Optional[datetime] = None
    
    def __init__(self, **data):
        super().__init__(**data)
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row, train_history=None):
        return cls(
            id=row["id"],
            modelName=row["modelname"],
            trainDetectionHistory=train_history if train_history else [],
            mapMetrix=row["mapmetrix"],
            isActive=row["isactive"],
            modelLink=row["modellink"],
            createDate=row["createdate"]
        )