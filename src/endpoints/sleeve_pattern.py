from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.sleeve_pattern import  SleevePattern,UpdateSleevePattern
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.sleeve_pattern as sleeve_pattern_rule

router = APIRouter(prefix="/sleeve_pattern", tags=["sleeve_pattern"])
@router.post("/add_sleeve_pattern", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_sub_category(request: Request, sleeve_pattern: SleevePattern = Body(...)):
    return sleeve_pattern_rule.create_sleeve_pattern(request,sleeve_pattern)

@router.put("/update_sleeve_pattern/{slv_ptn_id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product_type(request: Request,slv_ptn_id:str,update_sleeve_pattern:UpdateSleevePattern = Body(...)):
    return sleeve_pattern_rule.update_sleeve_pattern(request,slv_ptn_id,update_sleeve_pattern)

@router.post("/get_sleeve_pattern_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_type_list(request: Request, user: get_user_model = Body(...)):
    return sleeve_pattern_rule.get_sleeve_pattern_list(request,user)

@router.get("/get_sleeve_pattern_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_sleeve_pattern_dropdown_list(request: Request):
    return sleeve_pattern_rule.get_sleeve_pattern_dropdown_list(request)