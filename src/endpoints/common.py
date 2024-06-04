from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.product import  Product,UpdateProduct
from src.models.custom_model import  (response_return_model,get_product_type_user_model,get_product_list_model,
                                      get_new_arrivals_request, coupon_code_request)
import src.rules.common as common_rule

router = APIRouter(prefix="/common", tags=["common"])

@router.post("/get_product_type_list_for_user", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_type_list_for_user(request: Request, product_type: get_product_type_user_model = Body(...)):
    return common_rule.get_product_type_list_for_user(request,product_type)

@router.get("/get_sub_category_list_for_user/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_sub_category_list_for_user(request: Request, id:str):
    return common_rule.get_sub_category_list_for_user(request,id)
@router.get("/get_category_list_for_user", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_category_list_for_user(request: Request):
    return common_rule.get_category_list_for_user(request)
@router.post("/get_new_arrivals_product_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_new_arrivals_product_list(request: Request, get_Data: get_new_arrivals_request = Body(...)):
    return common_rule.get_new_arrivals_product_list(request,get_Data)

@router.post("/get_fabric_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_fabric_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_fabric_filter_list(request,filter_data)

@router.post("/get_size_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_size_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_size_filter_list(request,filter_data)
@router.post("/get_color_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_color_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_color_filter_list(request,filter_data)

@router.post("/get_price_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_price_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_price_filter_list(request,filter_data)

@router.post("/get_occasion_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_occasion_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_occasion_filter_list(request,filter_data)

@router.post("/get_sleeve_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_sleeve_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_sleeve_filter_list(request,filter_data)

@router.post("/get_neck_filter_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_neck_filter_list(request: Request,  filter_data: get_product_list_model = Body(...)):
    return common_rule.get_neck_filter_list(request,filter_data)

@router.post("/order_status_update", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def order_status_update(request: Request):
    return common_rule.order_status_update(request)

@router.post("/get_coupon_code_discount", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_coupon_code_discount(request: Request, filter_data: coupon_code_request = Body(...)):
    return common_rule.get_coupon_code_discount(request , filter_data)