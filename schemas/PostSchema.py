from pydantic import BaseModel, Field

class CreatePost(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=1000)

class ShowPosts(BaseModel):
    id: int
    title: str
    content: str
    user_id: int