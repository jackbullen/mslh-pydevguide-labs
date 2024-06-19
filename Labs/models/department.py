from pydantic import BaseModel

class Department(BaseModel):
    code: str     # ECE
    pid: str      # ryAe4JY7V
    name: str     # Department of Electrical and Computer Engineering
    faculty: str  # Engineering and Computer Science

    class Config:
        populate_by_name=True
    
    class Settings:
        name = "departments"