from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.neck_design import  NeckDesign,UpdateNeckDesign
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.neck_design as neck_design_rule

router = APIRouter(prefix="/neck_design", tags=["neck_design"])

@router.post("/add_neck_design", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_neck_design(request: Request, neck_design: NeckDesign = Body(...)):
    return neck_design_rule.create_neck_design(request,neck_design)

@router.put("/update_neck_design/{neck_dsgn_id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_neck_design(request: Request,neck_dsgn_id:str,update_neck_design:UpdateNeckDesign = Body(...)):
    return  neck_design_rule.update_neck_design(request,neck_dsgn_id,update_neck_design)

@router.post("/get_neck_design_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_fabric_type_list(request: Request, user: get_user_model = Body(...)):
    return neck_design_rule.get_neck_design_list(request,user)

@router.get("/get_neck_design_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_neck_design_dropdown_list(request: Request):
    return neck_design_rule.get_neck_design_dropdown_list(request)