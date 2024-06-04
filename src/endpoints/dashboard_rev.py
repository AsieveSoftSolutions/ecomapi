from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.custom_model import response_return_model, get_product_type_user_model, get_product_list_model, \
    get_new_arrivals_request
import src.rules.dashboard_rev as dashboardRev
from src.models.dashboard_rev import total_sales_request

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# @router.get("/get_revenue_items", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=response_return_model)
# def get_revenue_items(request: Request):
#     return dashboardRev.get_revenue_items(request)

@router.post("/get_revenue_items", response_description="Create a new user", status_code=status.HTTP_201_CREATED,
            response_model=response_return_model)
def get_revenue_item(request: Request,  filter_data: total_sales_request = Body(...)):
    return dashboardRev.get_revenue_items(request, filter_data)

@router.get("/get_category_amt_list", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_category_amt_list(request: Request):
    return dashboardRev.get_amt_by_category(request)

@router.get("/get_prod_amt", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_prod_amt(request: Request):
    return dashboardRev.get_amt_by_prod(request)

@router.get("/get_prdt_qnt", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_prdt_qnt(request: Request):
    return dashboardRev.get_qnt_by_prdt(request)

@router.get("/get_tot_profit", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_tot_profit(request: Request):
    return dashboardRev.get_total_profit(request)

@router.get("/get_profit_by_category", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_profit_by_category(request: Request):
    return dashboardRev.get_profit_for_category(request)


@router.get("/get_tot_qntt", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_tot_qntt(request: Request):
    return dashboardRev.get_total_quantity(request)

@router.get("/get_prod_sold", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_prod_sold(request: Request):
    return dashboardRev.get_total_product_sold(request)

@router.get("/get_expenses", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_expenses(request: Request):
    return dashboardRev.get_total_expenses(request)

@router.get("/get_profit_by_month", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_profit_by_month(request: Request):
    return dashboardRev.get_total_profit_by_month(request)

@router.get("/get_tot_sales", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_tot_sales(request:Request):
    return dashboardRev.get_total_sales(request)

@router.get("/get_tot_pft_by_prod", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_tot_pft_by_prod(request: Request):
    return dashboardRev.get_total_profit_by_product(request)

@router.get("/get_actual_cost", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_actual_cost(request: Request):
    return dashboardRev.get_total_actual_cost(request)

@router.get("/get_selling_cost", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_selling_cost(request: Request):
    return dashboardRev.get_total_selling_cost(request)

@router.get("/get_dashboard_revenue", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_dashboard_revenue(request: Request):
    return dashboardRev.get_dashboard_details(request)

@router.get("/get_product_type_filter", response_description="Create a new user", status_code=status.HTTP_201_CREATED,response_model=response_return_model)
def get_product_type_filter(request: Request):
    return dashboardRev.get_product_type_filters(request)
