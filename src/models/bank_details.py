import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class Bank_Details(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    user_id : str
    bank_id : str = Field(default="0")
    card_holder_name : str
    card_number : str
    month_year :str
    cvv_number : str
    is_active : int  = Field(default=1)
    created_date:datetime
    updated_date : datetime


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "CUS001",
                "bank_id":"0",
                "card_holder_name": "Krishnan",
                "card_number": "25001 0202 8546",
                "month_year": "08/2025",
                "cvv_number": "5216",
                "is_active":1,
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02"

            }
        }
class Update_bank_details(BaseModel):
    card_holder_name: Optional[str]
    card_number: Optional[str]
    month_year: Optional[str]
    cvv_number: Optional[str]
    is_active: Optional[str]