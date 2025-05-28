from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    id: Optional[str] = None
    roleName: Optional[str] = None
    
    class Config:
        from_attributes = True 