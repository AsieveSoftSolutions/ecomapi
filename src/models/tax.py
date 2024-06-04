import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class Tax(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    tax_id : str
    tax_name : str
    tax_percentage:float
    is_active : int  = Field(default=1)
    create_by:str
    update_by:str
    created_date:datetime
    updated_date : datetime


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "tax_id":"0",
                "tax_name": "GST",
                "tax_percentage":12,
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02",

            }
        }


class UpdateTax(BaseModel):
    tax_name: Optional[str]
    tax_percentage:Optional[float]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[str]
