from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.postal_service import  PostalService,UpdatePostalService
from src.models.custom_model import  response_return_model,get_user_model,get_user_postal_request

import src.rules.postal_service as postal_service_rule

router = APIRouter(prefix="/postal_service", tags=["postal_service"])

@router.post("/add_postal_service", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_postal_service(request: Request, postal: PostalService = Body(...)):
    return postal_service_rule.create_postal_service(request,postal)

@router.put("/update_postal_service/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_postal_service(request: Request,id:str,update_postal:UpdatePostalService = Body(...)):
    return  postal_service_rule.update_postal_service(request,id,update_postal)

@router.post("/get_postal_service_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_postal_service_list(request: Request, user: get_user_model = Body(...)):
    return postal_service_rule.get_postal_service_list(request,user)

@router.get("/get_postal_service_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_postal_service_dropdown_list(request: Request):
    return postal_service_rule.get_postal_service_dropdown_list(request)

@router.post("/get_user_postal_service_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_user_postal_service_list(request: Request, user: get_user_postal_request = Body(...)):
    return postal_service_rule.get_user_postal_service_list(request,user)

@router.get("/get_country_list/{types}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_country_list(request: Request,types:int):
    return postal_service_rule.get_country_list(request,types)