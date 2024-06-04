from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.brand import  Brand,UpdateBrand
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.brand as brand_rule

router = APIRouter(prefix="/brand", tags=["brand"])

@router.post("/add_brand", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_brand(request: Request, brand: Brand = Body(...)):
    return brand_rule.create_brand(request,brand)

@router.put("/update_brand/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_brand(request: Request,id:str,brand:UpdateBrand = Body(...)):
    return  brand_rule.update_brand(request,id,brand)

@router.post("/get_brand_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_brand_list(request: Request, user: get_user_model = Body(...)):
    return brand_rule.get_brand_list(request,user)
@router.get("/get_brand_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_brand_dropdown_list(request: Request):
    return brand_rule.get_brand_dropdown_list(request)