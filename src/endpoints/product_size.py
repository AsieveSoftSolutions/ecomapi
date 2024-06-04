from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.product_size import  ProductSize,UpdateProductSize
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.product_size as product_size_rule

router = APIRouter(prefix="/product_size", tags=["product_size"])

@router.post("/add_product_size", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_product_size(request: Request, product_type: ProductSize = Body(...)):
    return product_size_rule.create_product_size(request,product_type)

@router.put("/update_product_size/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product_size(request: Request,id:str,update_product_type:UpdateProductSize = Body(...)):
    return  product_size_rule.update_product_size(request,id,update_product_type)

@router.post("/get_product_size_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_size_list(request: Request, user: get_user_model = Body(...)):
    return product_size_rule.get_product_size_list(request,user)

@router.get("/get_product_size_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_size_dropdown_list(request: Request):
    return product_size_rule.get_product_size_dropdown_list(request)