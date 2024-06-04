from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.product_type import  ProductType,UpdateProductType
from src.models.custom_model import  response_return_model,get_product_type_model

import src.rules.product_type as product_type_rule

router = APIRouter(prefix="/product_type", tags=["product_type"])

@router.post("/add_product_type", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_sub_category(request: Request, product_type: ProductType = Body(...)):
    return product_type_rule.create_product_type(request,product_type)

@router.put("/update_product_type/{fab_type_id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product_type(request: Request,fab_type_id:str,update_product_type:UpdateProductType = Body(...)):
    return  product_type_rule.update_product_type(request,fab_type_id,update_product_type)

@router.post("/get_product_type_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_type_list(request: Request, product_type: get_product_type_model = Body(...)):
    return product_type_rule.get_product_type_list(request,product_type)

@router.get("/get_product_type_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_type_dropdown_list(request: Request):
    return product_type_rule.get_product_type_dropdown_list(request)