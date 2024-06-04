import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import List


class response_return_model(BaseModel):
    error_code: str
    message: str
    data: Optional[list]


class login_model(BaseModel):
    email: str
    password: str
    role: Optional[int]


class get_user_model(BaseModel):
    search: str
    limit: int
    skip_count: int
    is_active: Optional[int]
    country: Optional[str]
    postal_id: Optional[str]


class get_sub_Category_model(BaseModel):
    search: str
    limit: int
    skip_count: int
    category_id: str
    is_active: Optional[int]


class get_product_type_model(BaseModel):
    search: str
    limit: int
    skip_count: int
    category_id: str
    sub_Category_id: str
    is_active: Optional[int]


class get_product_model(BaseModel):
    search: str
    limit: int
    skip_count: int
    category_id: str
    sub_Category_id: str
    product_type_id: str


class get_product_list_model(BaseModel):
    search: str
    advertisement_id: str
    category: list
    sub_category: Optional[list]
    product_type: list
    size: list
    sleeve_pattern: list
    fabric_type: list
    price_start_range: float
    price_end_range: float
    occasion: list
    neck_design: list
    color: list
    user_id: str
    limit: Optional[int]
    skip: Optional[int]


class get_product_type_user_model(BaseModel):
    category: str
    sub_category: str


class get_product_details_model(BaseModel):
    product_id: str
    user_id: str


class get_ratting_model(BaseModel):
    product_id: str
    limit: int


class get_all_product_rating_model(BaseModel):
    search: str
    limit: int
    skip: int


class get_ratting_list_request(BaseModel):
    product_id: str
    rating_range: int
    type: int
    limit: int
    skip: int


class get_wishlist_cookies_request(BaseModel):
    product_id: list
    limit: int
    skip: int


class delete_wishList_request(BaseModel):
    product_id: str
    user_id: str


class get_wishlist_request(BaseModel):
    user_id: Optional[str]
    limit: int
    skip: int
    status: Optional[str]
    search: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]


class cart_quantity_update_request(BaseModel):
    cart_id: str
    type: str


class cart_check_request(BaseModel):
    card_id: list


class get_new_arrivals_request(BaseModel):
    user_id: str


class OrderDetails(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()).replace('-', ''))
    order_details_id: str
    order_id: str
    user_id: str
    product_id: str
    sub_product_id: str
    price: float
    total_price: float
    gst_price: float
    delivery_amount: float
    quantity: int
    delivery_status: str
    expected_delivery_date: str
    track_id: str
    postal_service_id: Optional[str] = Field(default='')
    ordered_date: str
    shipped_date: str
    delivery_date: str
    ratting_date: str
    is_active: int = Field(default=1)
    create_by: str
    update_by: str
    created_date: datetime
    updated_date: datetime


class UpdateOrderDetails(BaseModel):
    price: Optional[float]
    total_price: Optional[float]
    quantity: Optional[int]
    delivery_status: Optional[str]
    expected_delivery_date: Optional[str]
    track_id: Optional[str]
    postal_service_id: Optional[str]
    ordered_date: Optional[str]
    shipped_date: Optional[str]
    delivery_date: Optional[str]
    ratting_date: Optional[str]
    update_by: Optional[str]
    updated_date: Optional[datetime]


class change_password_request(BaseModel):
    user_id: Optional[str]
    old_pwd: Optional[str]
    new_pwd: Optional[str]


class get_user_postal_request(BaseModel):
    country: str


class get_user_delivery_request(BaseModel):
    postal_id: str
    weight: float


class get_orderid_request(BaseModel):
    amount: float
    currency: str
    receipt: str


class forget_pwd_request(BaseModel):
    email: str
    otp: str
    password: str
    type: int

class get_cookies_cart_list_request(BaseModel):
    product_id: str
    color: str
    size_id: str
    quantity: int

class refund_request_data(BaseModel):
    amount:float
    payment_id:str

class get_order_price_request(BaseModel):
    order_id:str
    order_details_id:str

class coupon_code_request(BaseModel):
    check_out_list:List[get_cookies_cart_list_request]
    coupon_code:str
