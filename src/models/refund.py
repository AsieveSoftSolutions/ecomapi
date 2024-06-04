import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List


class Refund(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    refund_id: str
    user_id: str
    product_id: str
    sub_product_id:str
    order_details_id:str
    refund_amount:float
    razorpay_refund_id:str
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "refund_id": "0",
                "user_id": "CUS001",
                "product_id": "PROD001",
                "sub_product_id":"SUBPROD001",
                "order_details_id":"",
                "refund_amount": 4,
                "razorpay_refund_id": "Good product",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",
            }
        }


class UpdateRefund(BaseModel):
    product_id: Optional[str]
    refund_amount:Optional[int]
    sub_product_id:Optional[str]
    razorpay_refund_id:Optional[str]
    order_details_id:Optional[str]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]
