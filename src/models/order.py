import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List
from src.models.custom_model import OrderDetails


class Order(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    order_id: str
    user_id: str
    price: float
    total_price:float
    delivery_amount:float
    quantity:int
    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    street: str
    pincode: str
    phone_number: str
    email: str
    transaction_status:str
    transaction_id:str
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime
    order_details:List[OrderDetails]
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "order_id": "0",
                "user_id": "CUS001",
                "price": 100,
                "total_price":100,
                "delivery_amount":50,
                "quantity":1,
                "first_name": "Karthik",
                "last_name": "Raja",
                "country": "India",
                "state": "Tamil Nadu",
                "city": "chennai",
                "street": "Adaiyar",
                "pincode": "636111",
                "phone_number": "9845761236",
                "email": "karthik@gmail.com",
                "transaction_id":"",
                "transaction_status":"",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date": "2023-11-24 12:24:02",
                "updated_date": "2023-11-24 12:24:02",
                "order_details":[{
                    "order_details_id":"",
                    "order_id":"",
                    "user_id":"",
                    "product_id":"",
                    "sub_product_id": "",
                    "price":100,
                    "total_price":100,
                    "delivery_amount":40,
                    "quantity":1,
                    "delivery_status":"",
                    "expected_delivery_date":"",
                    "is_active": 1,
                    "create_by": "CUS001",
                    "update_by": "CUS001",
                    "created_date": "2023-11-24 12:24:02",
                    "updated_date": "2023-11-24 12:24:02",
                }]
            }
        }


class UpdateOrder(BaseModel):
    sub_product_id: Optional[str]
    price: Optional[float]
    quantity:Optional[int]
    status: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    street: Optional[str]
    pincode: Optional[str]
    phone_number: Optional[str]
    transaction_status:Optional[str]
    transaction_id:Optional[str]
    email: Optional[str]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]


