
from dataclasses import dataclass
from datetime import date
from pydantic import BaseModel, Field
from .utils import Sex 

@dataclass
class PassportData(BaseModel):
    surname: str = Field(description="Surname of the license holder")
    given_names: str 
    date_of_birth: date 
    date_of_issue: date
    date_of_expiration: date 
    passport_no: str
    nationality: str
    place_of_birth: str 
    sex: Sex 
    authority: str 
