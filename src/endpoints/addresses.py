from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.addresses import UserAddress, UpdateAddress
from src.models.custom_model import  response_return_model


import src.rules.addresses as addresses


router = APIRouter(prefix="/address",
    tags=["Address"])

@router.post("/add_address", response_description="Create a new user address", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_addrs(request: Request, user_addrs: UserAddress = Body(...)):  
    return addresses.create_addrs(request, user_addrs)



@router.get("/get_user_address_list/{userid}", response_description="List addresses", response_model=response_return_model)
def list_addrs(request: Request, userid: str):
    return addresses.list_addrs(request,userid)

@router.get("/{user_id}", response_description="Get user's addresses", response_model=List[UserAddress])
def find_addrs(request: Request, user_id: str):    
    return addresses.find_addrs(request, user_id)

@router.put("/update_address/{id}", response_description="Update an address", response_model=response_return_model)
def update_addrs(request: Request, id: str, addrs: UpdateAddress = Body(...)):
    return addresses.update_addrs(request, id, addrs)

@router.delete("/delete_address/{id}", response_description="Delete an address by its id")
def delete_addrs(request: Request, id:str):
    return addresses.delete_addrs(request, id)
