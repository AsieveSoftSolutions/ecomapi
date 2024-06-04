from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.carts import Carts,UpdateCarts
from src.models.custom_model import  response_return_model,get_user_model,get_wishlist_request,cart_quantity_update_request,cart_check_request,get_cookies_cart_list_request
import src.rules.carts as carts_rule

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add_cart", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def add_cart(request: Request, cart: Carts = Body(...)):
    return carts_rule.add_cart(request,cart)

@router.put("/update_cart/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_cart(request: Request, id:str, cart: UpdateCarts = Body(...)):
    return carts_rule.update_cart(request,id,cart)

@router.delete("/delete_cart/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_cart(request: Request, id:str):
    return carts_rule.delete_cart(request,id)

@router.post("/get_cart_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_cart_list(request: Request, cart: get_wishlist_request = Body(...)):
    return carts_rule.get_cart_list(request,cart)
@router.post("/cart_quantity_check", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def cart_quantity_check(request: Request, cart: cart_check_request = Body(...)):
    return carts_rule.cart_quantity_check(request,cart)

@router.post("/cart_quantity_update", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_cart_quantity(request: Request, cart: cart_quantity_update_request = Body(...)):
    return carts_rule.update_cart_quantity(request,cart)

@router.post("/get_checkout_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_checkout_list(request: Request, cart: cart_check_request = Body(...)):
    return carts_rule.get_checkout_list(request,cart)

@router.get("/get_cart_count/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_cart_count(request: Request, id:str):
    return carts_rule.get_cart_count(request,id)

@router.post("/delete_multiple_cart", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_multiple_cart(request: Request,cart: cart_check_request = Body(...)):
    return carts_rule.delete_multiple_cart(request,cart)

@router.post("/get_cookies_cart_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_cookies_cart_list(request: Request,cart: List[get_cookies_cart_list_request] = Body(...)):
    return carts_rule.get_cookies_cart_list(request,cart)

@router.post("/cookie_cart_quantity_check", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def cookie_cart_quantity_check(request: Request, cart: List[get_cookies_cart_list_request] = Body(...)):
    return carts_rule.cookie_cart_quantity_check(request,cart)

@router.post("/get_cookie_checkout_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_cookie_checkout_list(request: Request, cart:  List[get_cookies_cart_list_request] = Body(...)):
    return carts_rule.get_cookie_checkout_list(request,cart)



