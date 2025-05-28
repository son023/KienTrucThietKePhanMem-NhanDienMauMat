from pydantic import BaseModel
from typing import Optional

class FullName(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    
    class Config:
        from_attributes = True 