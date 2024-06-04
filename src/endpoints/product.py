from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.product import  Product,UpdateProduct
from src.models.custom_model import  response_return_model,get_user_model,get_product_model,get_product_list_model,get_product_details_model
from src.models.sub_product import  UpdateSubProduct,SubProductList
import src.rules.product as product_rule

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/add_product", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_product(request: Request, product: Product = Body(...)):
    return product_rule.create_product(request,product)

@router.put("/update_product/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product(request: Request,id:str,update_product:UpdateProduct = Body(...)):
    return  product_rule.update_product(request,id,update_product)

@router.post("/get_product_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_list(request: Request,productModel:get_product_model = Body(...)):
    return  product_rule.get_product_list(request,productModel)

@router.post("/get_product_user_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product_user_list(request: Request,productListModel:get_product_list_model = Body(...)):
    return  product_rule.get_product_user_list(request,productListModel)

@router.post("/get_product_details", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_product(request: Request,product_details_model:get_product_details_model = Body(...)):
    return  product_rule.get_product(request, product_details_model)

@router.get("/get_similar_product_list/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_similar_product_list(request: Request,id:str):
    return  product_rule.get_similar_product_list(request,id)

@router.post("/update_sub_product", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_sub_product(request: Request,sup_product:UpdateSubProduct = Body(...)):
    return  product_rule.update_sub_product(request, sup_product)
@router.post("/add_sub_product", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def add_sub_product(request: Request,sup_product: SubProductList = Body(...)):
    return  product_rule.add_sub_product(request, sup_product)

@router.put("/update_product_only/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product_only(request: Request,id:str,update_product:UpdateProduct = Body(...)):
    return  product_rule.update_product_only(request,id,update_product)


@router.put("/delete_product/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_product(request: Request,id:str):
    return  product_rule.delete_product(request,id)

@router.put("/delete_sub_product/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def delete_sub_product(request: Request,id:str):
    return  product_rule.delete_sub_product(request,id)

@router.put("/update_product_is_ctive/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_product_is_ctive(request: Request,id:str,update_product:UpdateProduct = Body(...)):
    return  product_rule.update_product_is_ctive(request,id,update_product)