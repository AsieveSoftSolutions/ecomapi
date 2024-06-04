import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List

class SubCategory(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    category_id : str
    sub_Category_id:str
    sub_category_name : str
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
                "sub_category_name": "Woman",
                "is_active": 1,
                "create_by": "CUS001",
                "update_by": "CUS001",
                "created_date":"2023-11-24 12:24:02",
                "updated_date":"2023-11-24 12:24:02",

            }
        }


class UpdateSubCategory(BaseModel):
    category_id : Optional[str]
    sub_Category_id : Optional[str]
    sub_category_name: Optional[str]
    is_active: Optional[int]
    update_by: Optional[str]
    updated_date: Optional[datetime]

class MultipleUpdateSubCategory(BaseModel):
    sub_category_list:List[UpdateSubCategory]
