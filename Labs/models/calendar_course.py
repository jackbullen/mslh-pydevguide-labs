from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

CourseList = List[str]
Requirement = Union[str, Dict[str, Any]]
RequirementList = Union[CourseList, List[Requirement]]

class CalendarCourse(BaseModel):
    code: str = Field(alias="_id")
    pid: str                            # Id used by UVic
    link: str
    year: int                           # 1, 2, 3, 4, or 5
    faculty: str
    cal: str                            # undergrad or grad
    name: Optional[str] = None
    description: Optional[str] = None   
    hours: Optional[str] = None         # 3-0-0
    notes: Optional[str] = None
    prerequisites: Optional[RequirementList] = None
    prerequisite_course_list: Optional[CourseList] = Field(alias="prerequisiteCourseList")
    embedding: List[float]
    
    class Config:
        populate_by_name = True