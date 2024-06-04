import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class Wishlist(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    wishlist_id: str
    user_id: str
    product_id: str
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "wishlist_id": "0",
                "user_id": "CUS001",
                "product_id": "PROD001",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",

            }
        }


class UpdateWishlist(BaseModel):
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[str]
