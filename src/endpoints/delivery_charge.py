from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.delivery_charge import DeliveryCharge, UpdateDeliveryCharge
from src.models.custom_model import response_return_model,get_user_model,get_user_delivery_request

import src.rules.delivery_charge as delivery_charge_rule

router = APIRouter(prefix="/delivery_charge", tags=["delivery_charge"])

@router.post("/add_deliver_charge", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_delivery_charge(request: Request, insertData: DeliveryCharge = Body(...)):
    return delivery_charge_rule.create_delivery_charge(request,insertData)

@router.put("/update_deliver_charge/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_delivery_charge(request: Request,id:str,updateData:UpdateDeliveryCharge = Body(...)):
    return  delivery_charge_rule.update_delivery_charge(request,id,updateData)

@router.post("/get_deliver_charge_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_delivery_charge_list(request: Request, user: get_user_model = Body(...)):
    return delivery_charge_rule.get_delivery_charge_list(request,user)

@router.get("/get_deliver_charge_dropdown_list/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_delivery_charge_dropdown_list(request: Request):
    return delivery_charge_rule.get_delivery_charge_dropdown_list(request)

@router.post("/get_user_delivery_charge", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_user_delivery_charge(request: Request, user: get_user_delivery_request = Body(...)):
    return delivery_charge_rule.get_user_delivery_charge(request,user)