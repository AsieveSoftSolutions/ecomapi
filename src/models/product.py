import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from src.models.sub_product import  SubProduct,UpdateSubProduct
from typing import List

class Product(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    product_name: str
    description:str
    product_id:str
    category_id : str
    sub_Category_id:str
    product_type_id:str
    product_url:str
    occasion_id:str
    sleeve_Pattern_id:str
    fabric_type_id:str
    neck_design_id:str
    dress_length:float
    dress_weight:float
    fitting:str
    brand_id:str
    size_chart_image:str
    is_active : int  = Field(default=1)
    is_delete:int  = Field(default=1)
    sub_product :List[SubProduct]
    no_size:int
    create_by:str
    update_by:str
    created_date:datetime
    updated_date : datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "product_name":"lace Kurthi",
                "product_id":"0",
                "category_id":"0",
                "sub_Category_id":"0",
                "product_type_id":"0",
                "occasion_id":"0",
                "sleeve_Pattern_id":"0",
                "fabric_type_id":"0",
                "neck_design_id":"0",
                "dress_length":156.2,
                "dress_weight":120.5,
                "fitting":"fitting",
                "product_url":"url",
                "brand_id":"0",
                "size_chart_image":"image.png",
                "sub_product":[
                 { "sub_product_id": "0",
                "product_id":"0",
                "size_id": "0",
                "color": "#403d36",
                "images": ["image.png", "image2.png"],
                "price": 500.6,
                "quantity": 20,
                "total_quantity":20,
                "cost_per_item": 600.2,
                "profit": 200.4,
                "margin": "10%",
                   "expense": 1,
                "is_active": 1,
                "is_delete":1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",
                   }],
                "is_active": 1,
                "is_delete":1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02",

            }
        }


class UpdateProduct(BaseModel):
    product_name:Optional[str]
    category_id : Optional[str]
    sub_Category_id : Optional[str]
    product_type_id:Optional[str]
    occasion_id:Optional[str]
    sleeve_Pattern_id:Optional[str]
    fabric_type_id:Optional[str]
    neck_design_id:Optional[str]
    product_url:Optional[str]
    dress_length:Optional[float]
    dress_weight:Optional[float]
    fitting:Optional[str]
    brand_id:Optional[str]
    description:Optional[str]
    size_chart_image:Optional[str]
    is_active: Optional[int]
    is_delete:Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]
    sub_product:Optional[List[UpdateSubProduct]]

