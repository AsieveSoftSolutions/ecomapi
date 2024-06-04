import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List


class total_sales_request(BaseModel):
    from_date: str
    to_date: str

