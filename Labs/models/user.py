from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    """
    Logged in user model
    """
    id: int = Field(alias="_id")
    username: str
    password: str
    public: str
    name: str
    picture_url: Optional[str] = Field(alias="pictureUrl", default=None)
    chat_sessions: Optional[List[str]] = Field(alias="chatSessions", default=[])
    degree: Optional[str] = "Undeclared"
    degreeCode: Optional[str] = None
    specialization: Optional[str] = ""
    completedCourses: Optional[List[str]] = []

    class Config:
        populate_by_name = True