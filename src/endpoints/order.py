from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.order import Order, UpdateOrder
from src.models.custom_model import  (response_return_model,get_user_model,
                                      UpdateOrderDetails,get_wishlist_request,get_order_price_request)
from src.models.refund import Refund, UpdateRefund
import src.rules.order as order_rule

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/add_order", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_order(request: Request, order: Order = Body(...)):
    return order_rule.create_order(request,order)

@router.put("/update_order/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_order(request: Request, id: str, update_order: UpdateOrder = Body(...)):
    return order_rule.update_order(request, id, update_order)

@router.put("/update_order_details/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_order_details(request: Request, id: str, update_order: UpdateOrderDetails = Body(...)):
    return order_rule.update_order_details(request, id, update_order)
@router.post("/get_order_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_order_list(request: Request, user: get_user_model = Body(...)):
    return order_rule.get_order_list(request, user)

@router.post("/get_user_order_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_user_order_list(request: Request, requestData: get_wishlist_request = Body(...)):
    return order_rule.get_user_order_list(request, requestData)

@router.post("/get_order_details_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_order_details_list(request: Request, requestData: get_wishlist_request = Body(...)):
    return order_rule.get_order_details_list(request, requestData)

@router.get("/order_email_send", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def order_email_send(request: Request):
    return order_rule.order_refund_email_send(request,"orid-220f6f0da773440ea2a6b27ba3a89da9")

@router.post("/get_order_price", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_order_price(request: Request, requestData: get_order_price_request = Body(...)):
    return order_rule.get_order_price(request, requestData)

@router.post("/update_order_refund", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_order_refund(request: Request, requestData: Refund = Body(...)):
    return order_rule.update_order_refund(request, requestData)







