import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class DeliveryCharge(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    delivery_charge_id : str
    postal_service_id : str
    types:str
    kg:float
    delivery_charge:float
    is_active : int  = Field(default=1)
    create_by:str
    update_by:str
    created_date:datetime
    updated_date : datetime


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "delivery_charge_id": "0",
                "postal_service_id": "",
                "types": "normal",
                "kg": 1,
                "delivery_charge": 100,
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02",

            }
        }


class UpdateDeliveryCharge(BaseModel):
    postal_service_id: Optional[str]
    types:Optional[str]
    kg:Optional[float]
    delivery_charge:Optional[float]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[str]
