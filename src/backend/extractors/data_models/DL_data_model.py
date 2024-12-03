from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from .utils import Sex

class DriverLicenseData(BaseModel):
    surname: str 
    given_names: str 
    date_of_birth: date 
    date_of_issue: date 
    date_of_expiration: date
    dl_number: str
    state: str 
    address: str 
    sex: Sex 

