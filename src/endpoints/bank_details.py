from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.bank_details import Bank_Details ,Update_bank_details
from src.models.custom_model import  response_return_model


import src.rules.bank_details as Bank_detils


router = APIRouter(prefix="/Bank",
    tags=["Bank"])

@router.post("/Add_Bank_Details", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_bank(request: Request, Bank: Bank_Details = Body(...)):
    return Bank_detils.create_bank(request,Bank)

@router.get("/get_Bank_Details/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_bank_list(request: Request, id: str):
    return Bank_detils.get_bank_list(request, id)


@router.put("/Update_Bank_Details/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_bank(request: Request, id:str, Update_Bank: Update_bank_details = Body(...)):
    return Bank_detils.update_bank(request,id,Update_Bank)