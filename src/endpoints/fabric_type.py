from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.fabric_type import  FabricType,UpdateFabricType
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.fabric_type as fabric_type_rule

router = APIRouter(prefix="/fabric_type", tags=["fabric_type"])

@router.post("/add_fabric_type", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_fabric_type(request: Request, fabric_type: FabricType = Body(...)):
    return fabric_type_rule.create_fabric_type(request,fabric_type)

@router.put("/update_fabric_type/{prod_type_id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_fabric_type(request: Request,prod_type_id:str,update_fabric_type:UpdateFabricType = Body(...)):
    return  fabric_type_rule.update_fabric_type(request,prod_type_id,update_fabric_type)

@router.post("/get_fabric_type_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_fabric_type_list(request: Request, user: get_user_model = Body(...)):
    return fabric_type_rule.get_fabric_type_list(request,user)
@router.get("/get_fabric_type_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_fabric_type_dropdown_list(request: Request):
    return fabric_type_rule.get_fabric_type_dropdown_list(request)