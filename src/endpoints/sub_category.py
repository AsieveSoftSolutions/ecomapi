from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.sub_category import SubCategory,UpdateSubCategory
from src.models.custom_model import  response_return_model,get_user_model,get_sub_Category_model

import src.rules.sub_category as sup_category_rule

router = APIRouter(prefix="/sub_category", tags=["sub_category"])

@router.post("/add_sub_Category", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_sub_category(request: Request, subcategory: SubCategory = Body(...)):
    return sup_category_rule.create_sub_category(request,subcategory)

@router.get("/get_sub_category_dropdown_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_sub_category_dropdown_list(request: Request):
    return sup_category_rule.get_sub_category_dropdown_list(request)


# @router.post("/update_sub_Category", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
# def update_sub_category(request: Request, updatesubCategory: MultipleUpdateSubCategory= Body(...)):
#     return sup_category_rule.update_sub_category(request,updatesubCategory)

@router.put("/update_sub_category_name/{sub_cat_id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_subCategory_name(request: Request,sub_cat_id:str,update_subcategory:UpdateSubCategory = Body(...)):
    return  sup_category_rule.update_subCategory_name(request,sub_cat_id,update_subcategory)

@router.post("/get_sub_category_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_sub_category_list(request: Request, User: get_sub_Category_model = Body(...)):
    return sup_category_rule.get_sub_category_list(request,User)

@router.delete("/delete_sub_category/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_sub_category(request: Request, id:str):
    return sup_category_rule.delete_sub_category(request,id)
