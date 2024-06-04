from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.tax import Tax, UpdateTax
from src.models.custom_model import response_return_model,get_user_model

import src.rules.tax as tax_rule

router = APIRouter(prefix="/tax", tags=["tax"])

@router.post("/add_tax", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_tax(request: Request, postal: Tax = Body(...)):
    return tax_rule.create_tax(request,postal)

@router.put("/update_tax/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_tax(request: Request,id:str,update_tax:UpdateTax = Body(...)):
    return  tax_rule.update_tax(request,id,update_tax)

@router.post("/get_tax_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_tax_list(request: Request, user: get_user_model = Body(...)):
    return tax_rule.get_tax_list(request,user)

@router.get("/get_tax_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_tax_dropdown_list(request: Request):
    return tax_rule.get_tax_dropdown_list(request)