# entity/DetectEyeDataTrain.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .DetectEyeData import DetectEyeData

class DetectEyeDataTrain(BaseModel):
    id: Optional[int] = None
    detectEyeDatas: Optional[List[DetectEyeData]] = []
    dataTrainPath: str
    detailFilePath: str
    
    def __init__(self, **data):
        super().__init__(**data)
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_db_row(cls, row, detect_eye_datas=None):
        return cls(
            id=row["id"],
            detectEyeDatas=detect_eye_datas if detect_eye_datas else [],
            dataTrainPath=row["datatrainpath"],
            detailFilePath=row["detailfilepath"]
        )
