from pydantic import BaseModel
from typing import Optional
from .FullName import FullName
from .Role import Role

class Member(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    department: Optional[str] = None
    fullName: Optional[FullName] = None
    role: Optional[Role] = None
    isActive: Optional[bool] = True
    createDate: Optional[str] = None
    
    class Config:
        from_attributes = True 