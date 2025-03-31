from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)

class GetUser(BaseModel):
    id: int
    name: str
    email: str

class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None