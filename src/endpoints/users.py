from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.users import User,UpdateUser
from src.models.custom_model import  response_return_model, login_model as LgoinModel ,get_user_model ,change_password_request,get_new_arrivals_request,forget_pwd_request
from src.models.otp import Otp,UpdateOtp

import src.rules.users as users


router = APIRouter(prefix="/user", tags=["User"])

@router.post("/user_registeration", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def create_user(request: Request, user: User = Body(...)):  
    return users.create_user(request,user)

@router.post("/get_user_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def get_user_list(request: Request, User: get_user_model = Body(...)):
    return users.get_user_list(request,User)

@router.post("/user_login", response_description="User login", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def user_login(request: Request, login: LgoinModel = Body(...)):
    return users.user_login(request,login)

@router.get("/", response_description="List users", response_model=List[User])
def list_users(request: Request):
    return users.list_users(request, 100)

@router.get("/{id}", response_description="Get a single user by id", response_model=User)
def find_user(request: Request, id: str):    
    return users.find_user(request, id)

@router.delete("/{id}", response_description="Delete a user")
def delete_user(request: Request, id:str):
    return users.delete_user(request, id)

@router.get("/get_user/{id}", response_description="Get a single user by id", response_model=response_return_model)
def get_user(request: Request, id: str):
    return users.get_user(request, id)

@router.put("/update_user/{id}", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def update_user(request: Request,id:str,update_data:UpdateUser = Body(...)):
    return  users.update_user(request,id,update_data)

@router.post("/change_password", response_description="User login", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def password_change(request: Request, change_pwd: change_password_request = Body(...)):
    return users.password_change(request,change_pwd)

@router.post("/verify_email", response_description="User login", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def verify_email(request: Request, get_user: get_new_arrivals_request = Body(...)):
    return users.verify_email(request,get_user)

@router.post("/otp_generate", response_description="User login", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def otp_generate(request: Request, otp_data: Otp = Body(...)):
    return users.otp_generate(request,otp_data)
@router.post("/forget_pwd", response_description="User login", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
def forget_pwd(request: Request, forget_pwd: forget_pwd_request = Body(...)):
    return users.forget_pwd(request,forget_pwd)




