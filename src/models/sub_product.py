import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List

class SubProduct(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    sub_product_id : str
    product_id:str
    size_id:str
    color_family:str
    color:str
    images:list
    price:float
    quantity:int
    total_quantity: int
    cost_per_item:float
    profit:float
    margin:float
    expense: float
    is_active : int  = Field(default=1)
    is_delete:int  = Field(default=1)
    create_by:str
    update_by:str
    created_date:datetime
    updated_date : datetime


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "sub_product_id": "0",
                "product_id":"0",
                "size_id": "0",
                "color": "#403d36",
                "images": ["image.png", "image2.png"],
                "price": 500.6,
                "quantity": 20,
                "total_quantity":20,
                "cost_per_item": 600.2,
                "profit": 200.4,
                "margin": 10,
                "expense": 1,
                "is_active": 1,
                "is_delete":1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",

            }
        }


class UpdateSubProduct(BaseModel):
    sub_product_id: Optional[str]
    size_id : Optional[str]
    color_family:Optional[str]
    color : Optional[str]
    images:Optional[list]
    price:Optional[float]
    quantity:Optional[int]
    total_quantity: Optional[int]
    cost_per_item:Optional[float] 
    profit:Optional[float]
    margin:Optional[float]
    expense: Optional[float]
    is_delete:Optional[int]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]

class SubProductList(BaseModel):
    sub_product:List[SubProduct]
