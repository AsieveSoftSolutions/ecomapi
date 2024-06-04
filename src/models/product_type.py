import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


class ProductType(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    category_id : str
    sub_Category_id:str
    product_type_id:str
    product_type_name : str
    image:str
    is_active : int  = Field(default=1)
    create_by:str
    update_by:str
    created_date:datetime
    updated_date : datetime


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "category_id":"0",
                "sub_Category_id":"0",
                "product_type_id":"0",
                "product_type_name": "Kurthi",
                "image":"image.png",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02",

            }
        }


class UpdateProductType(BaseModel):
    category_id : Optional[str]
    sub_Category_id : Optional[str]
    product_type_name: Optional[str]
    image: Optional[str]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]