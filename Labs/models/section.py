from typing import Optional
from pydantic import BaseModel, Field

class Section(BaseModel):
    crn: str = Field(alias="_id")               # Course Reference Number (unique for each section) # alias doesnt do anything here cause Model never being made
    code: str                                   # Course which this section is for
    f2f: str                                    # Indicates face-to-face or online
    seq: str                                    # A01, A02, B01, T01, ...
    is_linked: bool = Field(alias="isLinked")   # Is the section linked to another one (Lab, Tutorial, ...)
    term: str                                   # 202409 or 202501
    start: Optional[str] = None                 # Start time
    end: Optional[str] = None                   # End time
    start_date: str = Field(alias="startDate")  # Start date
    end_date: str = Field(alias="endDate")      # End date
    type: str                                   # CLAS, ...
    description: str    
    days: str                                   # Day of week string: TWF, MTh, ...
    monday: bool                                # True or false if has meeting on Monday
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    # building: Optional[str] = None # leaving this out, not public
    # building_number: Optional[str] = Field(alias="buildingNumber")

    class Config:
        populate_by_name = True