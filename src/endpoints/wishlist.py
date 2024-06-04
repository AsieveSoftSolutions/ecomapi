from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.wishlist import Wishlist,UpdateWishlist
from src.models.custom_model import  response_return_model,get_user_model,get_wishlist_cookies_request, delete_wishList_request ,get_wishlist_request

import src.rules.wishlist as wishlist_rule

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("/add_wishlist", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def add_wishlist(request: Request, wish: Wishlist = Body(...)):
    return wishlist_rule.add_wishlist(request,wish)

@router.post("/delete_wishlist", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_wishlist(request: Request, wish: delete_wishList_request = Body(...)):
    return wishlist_rule.delete_wishlist(request,wish)

@router.post("/get_wishlist_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_wishlist_list(request: Request,  wish: get_wishlist_request = Body(...)):
    return wishlist_rule.get_wishlist_list(request,wish)

@router.post("/get_wishlist_for_cookies", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_wishlist_for_cookies(request: Request, wish_ids: get_wishlist_cookies_request = Body(...)):
    return wishlist_rule.get_wishlist_for_cookies(request,wish_ids)