import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from src.models.sub_product import SubProduct, UpdateSubProduct


class Advertisement(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    advertisement_id: str
    coupon_code: str
    offer_percentage: int
    advertisement_name: str
    image: str
    category_id: list
    sub_Category_id: list
    product_type_id: list
    occasion_id: list
    sleeve_Pattern_id: list
    fabric_type_id: list
    neck_design_id: list
    product_size_id: list
    validate_from: str
    validate_to: str
    product_from: str
    product_to: str
    is_active: int = Field(default=1)
    is_delete: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "advertisement_id": "0",
                "coupon_code": "PATRICK20",
                "offer_percentage": 5,
                "image": "image.png",
                "category_id": [],
                "sub_Category_id": [],
                "product_type_id": [],
                "occasion_id": [],
                "sleeve_Pattern_id": [],
                "fabric_type_id": [],
                "neck_design_id": [],
                "product_size_id": [],
                "validate_from": "2023-10-20",
                "validate_to": "2023-10-20",
                "product_from": "2023-10-20",
                "product_to": "2023-10-20",
                "is_active": 1,
                "is_delete": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",

            }
        }


class UpdateAdvertisement(BaseModel):
    coupon_code: Optional[str]
    offer_percentage: Optional[int]
    category_id: Optional[list]
    image: Optional[str]
    sub_Category_id: Optional[list]
    product_type_id: Optional[list]
    occasion_id: Optional[list]
    sleeve_Pattern_id: Optional[list]
    fabric_type_id: Optional[list]
    neck_design_id: Optional[list]
    product_size_id: Optional[list]
    product_to: Optional[str]
    validate_from: Optional[str]
    validate_to: Optional[str]
    product_from: Optional[str]
    product_to: Optional[str]
    is_active: Optional[int]
    is_delete: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]
