from pydantic import BaseModel, Field
from typing import Optional

class CreateCategory(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class ShowCategoty(BaseModel):
    id: int
    name: str
