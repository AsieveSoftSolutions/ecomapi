from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.category import Category,UpdateCategory
from src.models.custom_model import  response_return_model,get_user_model

import src.rules.category as category_rule

router = APIRouter(prefix="/category", tags=["category"])

@router.post("/Add_Category", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_category(request: Request, category: Category = Body(...)):
    return category_rule.create_category(request,category)


@router.post("/get_category_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_category_list(request: Request, User: get_user_model = Body(...)):
    return category_rule.get_category_list(request,User)
@router.put("/Update_Category/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_category(request: Request, id:str, update_categroy: UpdateCategory = Body(...)):
    return category_rule.update_category(request,id,update_categroy)

@router.get("/get_dropdown_category_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_dropdown_category_list(request: Request):
    return category_rule.get_dropdown_category_list(request)