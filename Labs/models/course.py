from typing import Any, Dict, Optional, List, Union
from pydantic import BaseModel, Field
from .section import Section

CourseList = List[str]
Requirement = Union[str, Dict[str, Any]]
RequirementList = Union[CourseList, List[Requirement]]

class Course(BaseModel):
    code: str = Field(alias="_id")              
    pid: str
    sections: List[Section]
    link: str
    year: int                                   
    term: str                                   # 202409 or 202501
    cal: str                                    # undergrad or grad
    name: str
    description: Optional[str]
    hours: Optional[str]
    notes: Optional[str]
    fall: int                                   # True of false if has sections in Fall term
    spring: int                                 #                                  Spring term
    similarity: Optional[float] = None          # Included if Course is a result of vector search
    prerequisites: Optional[RequirementList]
    prerequisite_course_list: Optional[CourseList] = Field(alias="prerequisiteCourseList")
    # faculty: list # leaving this out, not public

    class Config:
        populate_by_name = True