from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.advertisement import  Advertisement,UpdateAdvertisement
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.advertisement as advertisement_rule

router = APIRouter(prefix="/advertisement", tags=["advertisement"])

@router.post("/add_advertisement", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_product(request: Request, advertisement: Advertisement = Body(...)):
    return advertisement_rule.create_advertisement(request,advertisement)

@router.put("/update_advertisement/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_advertisement(request: Request,id:str,update_advertisement:UpdateAdvertisement = Body(...)):
    return  advertisement_rule.update_advertisement(request,id,update_advertisement)

@router.post("/get_advertisement_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_advertisement_list(request: Request, user: get_user_model = Body(...)):
    return advertisement_rule.get_advertisement_list(request,user)

@router.get("/get_active_advertisement_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_active_advertisement_list(request: Request):
    return advertisement_rule.get_active_advertisement_list(request)