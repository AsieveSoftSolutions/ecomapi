import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class Otp(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    otp_id: str
    email: str
    type: int
    otp: str
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "otp_id": "0",
                "email": "CUS001",
                "type":1,
                "otp":"1234",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",

            }
        }


class UpdateOtp(BaseModel):
    otp: Optional[str]
    email:Optional[str]
    type:Optional[int]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[str]
