from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class Specialization(BaseModel):
    pid: str
    title: str
    requirements: Optional[Dict[str, List]] = None
    notes: Optional[str] = ""
    description: Optional[str] = ""
    degree: str

CourseList = List[str]

class Degree(BaseModel):
    code: str = Field(alias="_id")      # BSC-ANSH
    title: str                          # Anthropology
    cred: str                           # Bachelor of Science
    link: str                           # Link to calendar
    description: Optional[str] = None   # Description of course
    notes: Optional[str] = None         # Administrative notes
    embedding: List[float]              # Vector embedding of title + description
    requirements: Optional[Dict[str, List]] = None # Maybe improve type here, but doesnt really matter.
    html_requirements: Optional[str] = None
    requirement_course_list: Optional[CourseList] = Field(alias="requirementCourseList")
    specializations: Optional[List[Specialization]] = None
    
    class Config:
        populate_by_name = True
