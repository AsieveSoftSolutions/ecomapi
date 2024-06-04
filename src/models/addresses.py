
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


class UserAddress(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: str
    address_id :str  = Field(default="1")
    first_name:str
    last_name : str
    country:str
    state: str
    city: str
    street: str
    pincode : str
    phone_number:str
    email:str
    is_active:int = Field(default=1)
    created_date:datetime
    updated_date : datetime
    
    class Config:
        schema_extra = {
            "example": {

                "user_id": "CUS001",
                "address_id": "0",
                "first_name": "Akash",
                "last_name": "babu",
                "country": "India",
                "state": "Tamil Nadu",
                "city": "Blablacity",
                "street": "Bablabla st",
                "pincode": "14350000",
                "phone_number": "8745961236",
                "email":"example@gmail.com",
                "is_active":1,
                "created_date":"2023-11-24 10:12:02",
                "updated_date": "2023-11-24 10:12:02"


            }
        }

class UpdateAddress(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    country:Optional[str]
    state:Optional[str]
    city:Optional[str]
    street:Optional[str]
    pincode:Optional[str]
    phone_number:Optional[str]
    email:Optional[str]
    updated_date:Optional[datetime]