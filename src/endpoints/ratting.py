from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.ratting import Ratting, UpdateRatting
from src.models.custom_model import  response_return_model,get_user_model,get_ratting_model,get_ratting_list_request

import src.rules.ratting as rating_rule

router = APIRouter(prefix="/ratting", tags=["ratting"])

@router.post("/add_ratting", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_ratting(request: Request, ratting: Ratting = Body(...)):
    return rating_rule.create_ratting(request,ratting)

@router.put("/update_ratting/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_ratting(request: Request, id: str, update_ratting: UpdateRatting = Body(...)):
    return rating_rule.update_ratting(request, id, update_ratting)

@router.post("/get_rating_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_rating_list(request: Request, ratting_model: get_ratting_model = Body(...)):
    return rating_rule.get_rating_list(request,ratting_model)

@router.post("/get_all_product_rating_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_all_product_rating_list(request: Request, ratting_model: get_user_model = Body(...)):
    return rating_rule.get_all_product_rating_list(request,ratting_model)

@router.post("/get_product_rating_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_rating_list(request: Request, ratting_model: get_ratting_list_request = Body(...)):
    return rating_rule.get_product_rating_list(request,ratting_model)