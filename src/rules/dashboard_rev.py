from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from typing import List
from datetime import datetime, timedelta
import src.config.credential as Credantial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import base64
from src.models.dashboard_rev import total_sales_request

def get_revenue_items(request: Request, filter_data: total_sales_request = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        fetch_data = request.app.database["order_details"]
        datas = list(fetch_data.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "total_sales": {
                            "$multiply": ["$total_price", "$quantity"]
                        },
                        "ordered_date": "$created_date"
                    }
                },
                {
                    "$group": {
                        "_id": 0,
                        "total_sales": {"$sum": "$total_sales"}
                    }
                }
            ]
        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = datas
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_category_amt(request: Request):
    return request.app.database["order_details"]

def get_amt_by_category(request: Request):
    response = {}
    try:
        category_list = list(get_category_amt(request).aggregate(
            [
                {
                    "$match": {
                        "is_delete": {"$ne": 1}
                    }
                },
                {
                    "$lookup": {
                        "from": "product",
                        "localField": "product_id",
                        "foreignField": "product_id",
                        "as": "product_details"
                    }
                },
                {
                    "$unwind": "$product_details"
                },
                {
                    "$lookup": {
                        "from": "product_type",
                        "localField": "product_details.product_type_id",
                        "foreignField": "product_type_id",
                        "as": "product_type_details"
                    }
                },
                {
                    "$unwind": "$product_type_details"  # Unwind the product_type_details array
                },
                {
                    "$group": {
                        "_id": "$product_details.product_type_id",
                        "product_type_name": {"$first": "$product_type_details.product_type_name"},
                        "total_sales": {"$sum": {"$multiply": ["$quantity", "$price"]}},
                        "total_expense": {"$sum": {"$add": ["$gst_price", "$delivery_amount"]}}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "product_type_id": "$_id",
                        "product_type_name": 1,
                        "total_sales": 1,
                        "total_expense": 1,
                        "total_profit": {"$subtract": ["$total_sales", "$total_expense"]}
                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_amt_prod(request:Request):
    return request.app.database["sub_product"]

def get_amt_by_prod(request: Request):
    response = {}
    try:
        prod_list = list(get_amt_prod(request).aggregate(
            [
                {
                    "$lookup": {
                        "from": "product",
                        "localField": "product_id",
                        "foreignField": "product_id",
                        "as": "products"
                    }
                },
                {
                    "$unwind": "$products"
                },
                {
                    "$lookup": {
                        "from": "product_type",
                        "localField": "products.product_type_id",
                        "foreignField": "product_type_id",
                        "as": "product_type"
                    }
                },
                {
                    "$unwind": "$product_type"
                },
                {
                    "$lookup": {
                        "from": "order_details",
                        "localField": "product_id",
                        "foreignField": "product_id",
                        "as": "order_details"
                    }
                },
                {
                    "$unwind": {
                        "path": "$order_details",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$lookup": {
                        "from": "sub_product",
                        "localField": "sub_product_id",
                        "foreignField": "sub_product_id",
                        "as": "sub_product"
                    }
                },
                {
                    "$unwind": {
                        "path": "$sub_product",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "product_type_id": "$products.product_type_id",
                            "product_type_name": "$product_type.product_type_name"
                        },
                        "total_sub_product_price": {"$sum": "$sub_product.price"},
                        "total_order_details_price": {"$sum": {"$ifNull": ["$order_details.total_price", 0]}}
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.product_type_name",
                        "product_type_id": {"$first": "$_id.product_type_id"},
                        "total_sub_product_price": {"$first": "$total_sub_product_price"},
                        "total_order_details_price": {"$first": "$total_order_details_price"}
                    }
                },
                {
                    "$project": {
                        "product_type_name": "$_id",
                        "product_type_id": 1,
                        "total_sub_product_price": 1,
                        "total_order_details_price": 1
                    }
                }
            ]

        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = prod_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_prdt_qnt(request: Request):
    return request.app.database["sub_product"]

def get_qnt_by_prdt(request: Request):
    response = {}
    try:
        product_qnt = list(get_prdt_qnt(request).aggregate([
            {
                "$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "products"
                }
            },
            {
                "$unwind": "$products"
            },
            {
                "$lookup": {
                    "from": "product_type",
                    "localField": "products.product_type_id",
                    "foreignField": "product_type_id",
                    "as": "product_type"
                }
            },
            {
                "$unwind": "$product_type"
            },
            {
                "$lookup": {
                    "from": "order_details",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "order_details"
                }
            },
            {
                "$unwind": {
                    "path": "$order_details",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$group": {
                    "_id": {
                        "product_type_id": "$products.product_type_id",
                        "product_type_name": "$product_type.product_type_name"
                    },
                    "quantity_available": { "$sum": "$quantity" },
                    "quantity_sold": { "$sum": { "$ifNull": ["$order_details.quantity", 0] } }
                }
            },
            {
                "$group": {
                    "_id": "$_id.product_type_name",
                    "product_type_id": { "$first": "$_id.product_type_id" },
                    "quantity_available": { "$first": "$quantity_available" },
                    "quantity_sold": { "$first": "$quantity_sold" }
                }
            },
            {
                "$project": {
                    "product_type_name": "$_id",
                    "product_type_id": 1,
                    "quantity_available": 1,
                    "quantity_sold": 1
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = product_qnt

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_tot_prft(request: Request):
    return request.app.database["order_details"]

def get_total_profit(request: Request):
    response = {}
    try:
        profit_by_category = list(get_tot_prft(request).aggregate(
            [
                {
                    "$lookup": {
                        "from": "order_details",
                        "localField": "sub_product_id",
                        "foreignField": "sub_product_id",
                        "as": "sub_product_details"
                    }
                },
                {
                    "$unwind": "$sub_product_details"
                },
                {
                    "$addFields": {
                        "total_cost": {
                            "$sum": [
                                "$sub_product_details.cost_per_item",
                                "$expense",
                                "$gst_price",
                                "$delivery_amount"
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "product_id": 1,
                        "price": 1,
                        "total_cost": 1,
                        "total_profit": {
                            "$subtract": [
                                "$price",
                                "$total_cost"
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$product_id",
                        "total_profit": {
                            "$sum": "$total_profit"
                        }
                    }
                },
                {
                    "$group": {
                        "_id": 0,
                        "total_profit": {
                            "$sum": "$total_profit"
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "total_profit": 1
                    }
                }
            ]

        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = profit_by_category

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_category_profit(request: Request):
    return request.app.database["order_details"]

def get_profit_for_category(request: Request):
    response = {}
    try:
        category_sales_list = list(get_category_profit(request).aggregate([
            {
                "$lookup": {
                    "from": "sub_product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "new_order_details"
                }
            },
            {
                "$unwind": "$new_order_details"
            },
            {
                "$lookup": {
                    "from": "product",
                    "localField": "new_order_details.product_id",
                    "foreignField": "product_id",
                    "as": "new_product"
                }
            },
            {
                "$unwind": "$new_product"
            },
            {
                "$lookup": {
                    "from": "product_type",
                    "localField": "new_product.product_type_id",
                    "foreignField": "product_type_id",
                    "as": "new_product_type"
                }
            },
            {
                "$unwind": "$new_product_type"
            },
            {
                "$addFields": {
                    "total_expense": {
                        "$sum": [
                            "$cost_per_item",
                            "$new_product_type.expense",
                            "$gst_price",
                            "$delivery_amount"
                        ]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "product_type_name": "$new_product_type.product_type_name",
                    "total_expense": 1,
                    "price": 1,
                    "profit": {
                        "$subtract": [
                            "$price",
                            "$total_expense"
                        ]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$product_type_name",
                    "total_expense": {"$sum": "$total_expense"},
                    "profit": {"$sum": "$profit"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "product_type_name": "$_id",
                    "total_expense": 1,
                    "profit": 1
                }
            }
        ]))

        response["error_code"] = '9999'
        response["message"] = "Successfully"
        response["data"] = category_sales_list

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_tot_quantity(request: Request):
    return request.app.database["sub_product"]

def get_total_quantity(request: Request):
    response = {}
    try:
        total_quantity = list(get_tot_quantity(request).aggregate(
            [
                {
                    "$group": {
                        "_id": 0,
                        "total_quantity": {"$sum": "$quantity"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "total_quantity": 1
                    }
                }
            ]
        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = total_quantity

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_tot_prod_sold(request: Request):
    return request.app.database["order_details"]

def get_total_product_sold(request: Request): 
    response = {}
    try:
        product_sold = list(get_tot_prod_sold(request).aggregate(
            [
                {
                    "$group": {
                        "_id": 0,
                        "total_quantity": {"$sum": "$quantity"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "total_quantity": 1
                    }
                }
            ]
        ))

        response["error_code"] = "9999"
        response["message"] = "Successful"
        response["data"] = product_sold

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


def get_tot_exp(request: Request):
    return request.app.database["order_details"]

def get_total_expenses(request: Request):
    response = {}
    try:

        total_expenses = list(get_tot_exp(request).aggregate([
            {
                "$group": {
                    "_id": 0,
                    "tot_expense": {"$sum": {"$add": ["$gst_price", "$delivery_amount"]}}
                }
            },
            {
                "$project": {
                    "tot_expense": 1,
                    "_id": 0
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successful"
        response["data"] = total_expenses

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_prft_by_mnt(request: Request):
    return request.app.database["order_details"]

def get_total_profit_by_month(request: Request):
    response = {}
    try:
        month_wise_profit = list(get_prft_by_mnt(request).aggregate([
            {
                "$addFields": {
                    "parsed_date": {
                        "$dateFromString": {"dateString": "$ordered_date"}
                    },
                    "profit": {
                        "$subtract": [
                            {"$multiply": ["$quantity", "$price"]},
                            {"$add": ["$gst_price", "$delivery_amount"]}
                        ]
                    }
                }
            },
            {
                "$project": {
                    "month": {"$month": "$parsed_date"},
                    "year": {"$year": "$parsed_date"},
                    "profit": 1
                }
            },
            {
                "$project": {
                    "formatted_date": {
                        "$concat": [
                            {"$toString": "$month"},
                            " '",
                            {"$substr": [{"$toString": "$year"}, 2, -1]}
                        ]
                    },
                    "profit": 1
                }
            },
            {
                "$group": {
                    "_id": "$formatted_date",
                    "total_profit": {"$sum": "$profit"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "ordered_date": "$_id",
                    "total_profit": 1
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successful"
        response["data"] = month_wise_profit

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_tot_sal(request: Request):
    return request.app.database["order_details"]

def get_total_sales(request:Request):
    response = {}

    try:
        tot_sales = list(get_tot_sal(request).aggregate(
            [
                {
                    "$addFields": {
                        "created_date": {"$toDate": "$created_date"}
                    }
                },
                {
                    "$project": {
                        "month": {"$month": "$created_date"},
                        "total_amount": {"$multiply": ["$quantity", "$total_price"]}
                    }
                },
                {
                    "$group": {
                        "_id": "$month",
                        "total_sales": {"$sum": "$total_amount"}
                    }
                }
            ]
        ))
        response["error_code"] = "9999"
        response["message"] = "Successful"
        response["data"] = tot_sales

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


# def get_tot_prft_by_prod(request: Request):
#     return request.app.database["sub_product"]
#
# def get_total_profit_by_product(request):
#     response = {}
#     try:
#         profit_by_product = list(get_tot_prft_by_prod(request).aggregate(
#             [
#                 {
#                     "$match": {
#                         "is_delete": 1
#                     }
#                 },
#                 {
#                     "$group": {
#                         "_id": 0,
#                         "profit_by_products": {
#                             "$sum": {
#                                 "$multiply": ["$profit", "$total_quantity"]
#                             }
#                         }
#                     }
#                 },
#                 {
#                     "$project": {
#                         "_id": 0,
#                         "profit_by_products": 1
#                     }
#                 }
#             ]
#         ))
#
#         response["error_code"] = "9999"
#         response["message"] = "Success"
#         response["data"] = profit_by_product
#
#     except Exception as e:
#         response["error_code"] = "0000"
#         response["message"] = str(e)
#
#     return response

def get_act_cost(request: Request):
    return request.app.database["sub_product"]

def get_total_actual_cost(request):
    response = {}
    try:
        actual_cost = list(get_act_cost(request).aggregate(
            [
                {
                    "$match": {
                        "is_delete": 1
                    }
                },
                {
                    "$group": {
                        "_id": 0,
                        "actual_cost": {
                            "$sum": {
                                "$multiply": ["$cost_per_item", "$total_quantity"]
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "actual_cost": 1
                    }
                }
            ]
        ))

        response["error_code"] = "9999"
        response["message"] = "Success"
        response["data"] = actual_cost

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_sell_cost(request: Request):
    return request.app.database["sub_product"]

def get_total_selling_cost(request):
    response = {}
    try:
        selling_cost = list(get_sell_cost(request).aggregate(
            [
                {
                    "$match": {
                        "is_delete": 1
                    }
                },
                {
                    "$group": {
                        "_id": 0,
                        "selling_cost": {
                            "$sum": {
                                "$multiply": ["$price", "$total_quantity"]
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "selling_cost": 1
                    }
                }
            ]
        ))

        response["error_code"] = "9999"
        response["message"] = "Success"
        response["data"] = selling_cost

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


    ############################### Single API for Dashboard ######################################

def get_dashboard_revenue(request: Request):
    return request.app.database["order_details"]

def get_dashboard_details(request):
    response = {}
    try:
        dashboard_revenue = list(get_dashboard_revenue(request).aggregate(
            [

            ]
        ))

        response["error_code"] = "9999"
        response["message"] = "Data Fetched Successfully"
        response["data"] = dashboard_revenue

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response

def get_prd_type_filter(request: Request):
    return request.app.database["product_type"]

def get_product_type_filters(request):
    response = {}
    try:
        product_type_filter = list(get_prd_type_filter(request).aggregate([
            {
                "$project": {
                    "_id": 0,
                    "product_type_name": "$product_type_name"  # Include the product_type_name field
                }
            }
        ]
        ))

        response["error_code"] = "9999"
        response["message"] = "Success"
        response["data"] = product_type_filter

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response
