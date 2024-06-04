from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.occasion import  Occasion,UpdateOccasion
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.occasion as occasion_rule

router = APIRouter(prefix="/occasion", tags=["occasion"])

@router.post("/add_occasion", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_occasion(request: Request, occasion: Occasion = Body(...)):
    return occasion_rule.create_occasion(request,occasion)

@router.put("/update_occasion/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_occasion(request: Request,id:str,update_occasion:UpdateOccasion = Body(...)):
    return  occasion_rule.update_occasion(request,id,update_occasion)

@router.post("/get_occasion_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_occasion_list(request: Request, user: get_user_model = Body(...)):
    return occasion_rule.get_occasion_list(request,user)

@router.get("/get_occasion_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_occasion_dropdown_list(request: Request):
    return occasion_rule.get_occasion_dropdown_list(request)