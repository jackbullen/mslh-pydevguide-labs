from pydantic import BaseModel, Field

class CompletedCourse(BaseModel):
    """
    Course that has been completed by the user
    Used for courses input by user or found in transcript
    """
    code: str                                           # MATH101
    title: str                                          # Calculus I
    grade: int                                          # 51
    grade_letter: str = Field(alias="gradeLetter")      # D
    grade_point: int = Field(alias="gradePoint")        # 1
    credits: float                                      # 1.5

    class Config:
        populate_by_name=True