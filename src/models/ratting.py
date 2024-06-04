import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List


class Ratting(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    ratting_id: str
    user_id: str
    product_id: str
    sub_product_id:str
    order_details_id:str
    ratting_value: int
    feedback: str
    image:list
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "ratting_id": "0",
                "user_id": "CUS001",
                "product_id": "PROD001",
                "sub_product_id":"SUBPROD001",
                "order_details_id":"",
                "ratting_value": 4,
                "image":["image.png"],
                "feedback": "Good product",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",
            }
        }


class UpdateRatting(BaseModel):
    product_id: Optional[str]
    ratting_value:Optional[int]
    sub_product_id:Optional[str]
    image:Optional[list]
    feedback:Optional[str]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]

# class ListOrder(BaseModel):
#     order_list = List[Order]
