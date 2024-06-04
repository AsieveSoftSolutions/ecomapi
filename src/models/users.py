import uuid
from pydantic import BaseModel, Field, SecretStr
from pydantic.networks import EmailStr
from datetime import date, datetime
from bson.objectid import ObjectId
from typing import Optional

class User(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    user_id: str = Field(default="0")
    user_name: str
    email: EmailStr = Field(unique=True, index=True)
    phone_no:str
    password: str
    gender:str
    profile:str
    date_of_birth:str
    last_name:str
    verify_status: Optional[int] = Field(default=0)
    created_by :str = Field(default="1")
    create_date :datetime
    updated_by: str = Field(default="1")
    update_date :datetime
    is_active : int  = Field(default=1)
    role:int = Field(default=1)




    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id":"0",
                "user_name":"",
                "last_name":"",
                "email":"",
                "phone_no":"",
                "password":"",
                "gender":"",
                "date_of_birth":"",
                "created_by":"",
                "updated_by": "",
                "create_date":"2023-11-23 10:01:01",
                "update_date":"2023-11-23 10:01:01",
                "is_active":1,
                "role":1,
                "profile":'image.png'
            }
        }

class UpdateUser(BaseModel):
    user_name:Optional[str]
    email:Optional[str]
    password:Optional[str]
    phone_no:Optional[str]
    gender:Optional[str]
    profile:Optional[str]
    date_of_birth:Optional[str]
    last_name:Optional[str]
    verify_status: Optional[int]
    updated_by:Optional[str]
    update_date:Optional[str]

