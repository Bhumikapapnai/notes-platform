from pydantic import BaseModel, EmailStr
from typing import Optional
#to validate all the entries are valid
class UserCreate(BaseModel):
    name: str
    email: EmailStr #check email is correct or not 
    password: str

class ResourceCreate(BaseModel):
    title: str
    subject: str
    semester: int
    resource_type: str   # "notes" ya "pyq"
    year: Optional[int]   # PYQ ke liye year, notes ke liye optional

class ResourceOut(BaseModel):
    id: int
    title: str
    subject: str
    semester: int
    resource_type: str
    year: Optional[int] 
    file_url: str
    uploader_id: int

    class Config:
        from_attributes = True