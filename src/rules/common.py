from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.custom_model import (response_return_model, get_product_type_user_model, get_product_list_model
,get_new_arrivals_request,coupon_code_request)
from bson import ObjectId
from typing import List
from datetime import datetime, timedelta
import src.config.credential as Credantial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import base64


def get_collection_product_type(request: Request):
    return request.app.database["product_type"]
def get_collection_sub_category(request: Request):
    return request.app.database["sub_category"]
def get_collection_category(request: Request):
    return request.app.database["category"]
def get_collection_product(request: Request):
    return request.app.database["product"]
def get_collection_order_details(request: Request):
    return request.app.database["order_details"]

def get_collection_advertisement(request: Request):
    return request.app.database["advertisement"]


def get_product_type_list_for_user(request: Request, product_type: get_product_type_user_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(product_type)
        resultData = list(get_collection_product_type(request).aggregate(
            [{"$match": {"$and": [{"is_active": 1}, {"category_id": filterData["category"]},
                                  {"$expr": {
                                      "$cond": {"if": {"$ne": [filterData["sub_category"], ""]}, "then":
                                          {"$eq": [filterData["sub_category"], "$sub_Category_id"]},
                                                "else": "true"}}},
                                  ]}},
             {"$lookup": {
                 "from": "product",
                 # "localField": "product_type_id",
                 # "foreignField": "product_type_id",
                 "let": {"product_type": "$product_type_id"},
                 "pipeline": [

                     {"$match": {"$expr": {"$and": [
                         {"$eq": ["$product_type_id", "$$product_type"]},
                         {"$eq": ['$is_delete', 1]},
                         {"$eq": ['$is_active', 1]}
                     ]
                     }
                     }},
                 ],
                 "as": "product"
             }},
             {"$match": {
                 "$expr": {"$gt": [
                     {"$size": "$product"},
                     0
                 ]}
             }},

             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "category_id": 1,
                     "sub_Category_id": 1,
                     "product_type_name": 1,
                     "product_type_id": 1,
                     "is_active": 1,
                     "image": 1,

                 }
             }

             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
def get_sub_category_list_for_user(request: Request, id:str):
    response = {}
    try:

        resultData = list(get_collection_sub_category(request).aggregate(
            [{"$match": {"$and": [{"is_active": 1}, {"category_id": id} ]}},
             {"$lookup": {
                 "from": "product",
                 # "localField": "product_type_id",
                 # "foreignField": "product_type_id",
                 "let": {"sub_category": "$sub_Category_id"},
                 "pipeline": [

                     {"$match": {"$expr": {"$and": [
                         {"$eq": ["$sub_Category_id", "$$sub_category"]},
                         {"$eq": ['$is_delete', 1]},
                         {"$eq": ['$is_active', 1]}
                     ]
                     }
                     }},
                 ],
                 "as": "product"
             }},
             {"$match": {
                 "$expr": {"$gt": [
                     {"$size": "$product"},
                     0
                 ]}
             }},

             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "category_id": 1,
                     "sub_Category_id": 1,
                     "sub_category_name": 1,
                     "is_active": 1,

                 }
             }

             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
def get_category_list_for_user(request: Request):
    response = {}
    try:

        resultData = list(get_collection_category(request).aggregate(
            [{"$match": {"$and": [{"is_active": 1}]}},
             {"$lookup": {
                 "from": "product",
                 # "localField": "product_type_id",
                 # "foreignField": "product_type_id",
                 "let": {"category": "$category_id"},
                 "pipeline": [

                     {"$match": {"$expr": {"$and": [
                         {"$eq": ["$category_id", "$$category"]},
                         {"$eq": ['$is_delete', 1]},
                         {"$eq": ['$is_active', 1]}
                     ]
                     }
                     }},
                 ],
                 "as": "product"
             }},
             {"$match": {
                 "$expr": {"$gt": [
                     {"$size": "$product"},
                     0
                 ]}
             }},

             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "category_id": 1,
                     "category_name": 1,
                     "is_active": 1,

                 }
             }

             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
def get_new_arrivals_product_list(request: Request, postData: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(postData)
        productList = list(get_collection_product(request).aggregate(
            [{"$match": {"$and": [
                {"is_active": 1},
                {"is_delete": 1}
            ]}},
                {"$lookup": {
                    "from": "sub_product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {"$match": {
                    "$expr": {"$gt": [
                        {"$size": "$sub_product"},
                        0
                    ]}
                }},
                {
                    "$sort": {"created_date": -1}
                }, {
                "$limit": 10
            },
                {"$lookup": {
                    "from": "wishlist",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [{"$eq": ["$user_id", filterData["user_id"]]},
                                                       {"$eq": ["$product_id", "$$product"]}]
                                              }
                                    }}
                    ],
                    "as": "wishlist"
                }},
                {"$addFields":

                     {"totalQuantity": {"$sum": "$sub_product.quantity"}

                      }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "category_id": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "product_name": 1,
                        "product_id": 1,
                        "is_active": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "dress_length": 1,
                        "dress_weight": 1,
                        "fitting": 1,
                        "sub_product.sub_product_id": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.size_id": 1,
                        "sub_product.color": 1,
                        "sub_product.images": 1,
                        "sub_product.price": 1,
                        "sub_product.quantity": 1,
                        "sub_product.cost_per_item": 1,
                        "sub_product.profit": 1,
                        "sub_product.margin": 1,
                        "totalQuantity": 1,
                        "wishlist.is_active": 1,
                    }
                }

            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = productList

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def query_build(postModel, filterType, request):
    response = {}
    try:
        getProduct = postModel

        advertisementList = []
        if getProduct["advertisement_id"] != "":
            advertisementList = list(get_collection_advertisement(request).aggregate([
                {"$match": {"advertisement_id": getProduct["advertisement_id"]}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "coupon_code": 1,
                        "offer_percentage": 1,
                        "advertisement_name": 1,
                        "category_id": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "product_size_id": 1,
                        "validate_from": 1,
                        "validate_to": 1,
                        "product_from": 1,
                        "product_to": 1,
                    }
                }
            ]))

        else:
            advertisement = {}
            advertisement["validate_from"] = ""
            advertisement["validate_to"] = ""

            advertisementList.append(advertisement)

        retVal = advertisementList[0].get("sleeve_Pattern_id")
        if retVal is not None:
            getProduct["sleeve_pattern"] = getProduct["sleeve_pattern"] + advertisementList[0]["sleeve_Pattern_id"]
            getProduct["product_type"] = getProduct["product_type"] + advertisementList[0]["product_type_id"]
            getProduct["category"] = getProduct["category"] + advertisementList[0]["category_id"]
            getProduct["fabric_type"] = getProduct["fabric_type"] + advertisementList[0]["fabric_type_id"]
            getProduct["occasion"] = getProduct["occasion"] + advertisementList[0]["occasion_id"]
            getProduct["neck_design"] = getProduct["neck_design"] + advertisementList[0]["neck_design_id"]
            if getProduct["sub_category"] is not None:
                getProduct["sub_category"] = getProduct["sub_category"] + advertisementList[0]["sub_Category_id"]
            else:
                getProduct["sub_category"] = advertisementList[0]["sub_Category_id"]
            getProduct["size"] = getProduct["size"] + advertisementList[0]["product_size_id"]
        Query = [{"is_active": 1}, {"is_delete": 1},
                 {"product_name": {"$regex": getProduct["search"], "$options": "i"}},
                 {"$expr": {
                     "$cond": {"if": {"$ne": [advertisementList[0]["validate_from"], ""]}, "then":
                         {"$lte": [advertisementList[0]["validate_from"], "$created_date"]},
                               "else": "true"}}},
                 {"$expr": {
                     "$cond": {"if": {"$ne": [advertisementList[0]["validate_to"], ""]}, "then":
                         {"$gte": [advertisementList[0]["validate_to"], "$created_date"]},
                               "else": "true"}}},
                 # {"$expr": {
                 #     "$cond": {"if": {"$ne": [advertisementList[0]["occasion_id"], "0"]}, "then":
                 #         {"$eq": [advertisementList[0]["occasion_id"], "$occasion_id"]},
                 #               "else": "true"}}},
                 # {"$expr": {
                 #     "$cond": {"if": {"$ne": [advertisementList[0]["neck_design_id"], "0"]}, "then":
                 #         {"$eq": [advertisementList[0]["neck_design_id"], "$neck_design_id"]},
                 #               "else": "true"}}}
                 ]
        if filterType != "sleeve":
            if len(getProduct["sleeve_pattern"]) > 0:
                Query.append({"sleeve_Pattern_id": {"$in": getProduct["sleeve_pattern"]}})
        if len(getProduct["product_type"]) > 0:
            Query.append({"product_type_id": {"$in": getProduct["product_type"]}})
        if filterType != "fabric":
            if len(getProduct["fabric_type"]) > 0:
                Query.append({"fabric_type_id": {"$in": getProduct["fabric_type"]}})
        if len(getProduct["category"]) > 0:
            Query.append({"category_id": {"$in": getProduct["category"]}})
        if filterType != "occasion":
            if len(getProduct["occasion"]) > 0:
                Query.append({"occasion_id": {"$in": getProduct["occasion"]}})
        if filterType != "neck":
            if len(getProduct["neck_design"]) > 0:
                Query.append({"neck_design_id": {"$in": getProduct["neck_design"]}})
        Query2 = [{"$eq": ["$product_id", "$$product"]},
                  # {
                  #     "$cond": {"if": {"$gt": [getProduct["price_end_range"], 1]}, "then":
                  #         {"$price": {"$gte":getProduct["price_end_range"],"$lt":getProduct["price_end_range"]}},
                  #               "else": "true"}}
                  # {"price": {"$gte": getProduct["price_start_range"], "$lt": getProduct["price_end_range"]}}
                  {"$cond": {"if": {"$eq": [filterType, "priceFilter"]}, "then":
                      "true", "else": {"$gte": ["$price", getProduct["price_start_range"]]}}},
                  {"$cond": {"if": {"$eq": [filterType, "priceFilter"]}, "then":
                      "true", "else":
                                 {
                                     "$cond": {"if": {"$gt": [getProduct["price_end_range"], 1]}, "then":
                                         {"$lte": ["$price", getProduct["price_end_range"]]},
                                               "else": "true"}}}}
                  ]
        if filterType != "size":
            if len(getProduct["size"]) > 0:
                Query2.append({"$in": ["$size_id", getProduct["size"]]})
        if filterType != "color":
            if len(getProduct["color"]) > 0:
                Query2.append({"$in": ["$color_family", getProduct["color"]]})
        queryList = []
        queryDis = {}
        queryDis["Query1"] = Query
        queryDis["Query2"] = Query2
        queryList.append(queryDis)
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = queryList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_fabric_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "fabric"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},

                    "pipeline": [

                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {"$lookup": {
                    "from": "fabric_type",
                    "localField": "fabric_type_id",
                    "foreignField": "fabric_id",
                    "as": "fabric_type"
                }},
                {
                    "$unwind": "$fabric_type"
                },
                {"$group": {
                    "_id": {
                        "fabric_type_id": "$fabric_type_id",
                    },
                    "fabric_type_id": {
                        "$first": "$fabric_type_id",
                    },
                    "fabric_name": {
                        "$first": "$fabric_type.fabric_name"
                    }
                }},
                {
                    "$project": {
                        "_id": 0,
                        "fabric_type_id": 1,
                        "fabric_name": 1,
                    }
                }

            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_size_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "size"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},

                    "pipeline": [

                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {
                    "$unwind": "$sub_product"
                },
                {"$group": {
                    "_id": {
                        "fabric_type_id": "$sub_product.size_id",
                    },
                    "size_id": {
                        "$first": "$sub_product.size_id",
                    },
                    "size_name": {
                        "$first": "$sub_product.product_size.size_Name"
                    }
                }},
                {
                    "$project": {
                        "_id": 0,
                        "size_id": 1,
                        "size_name": 1,
                    }
                }

            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_color_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "color"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},

                    "pipeline": [

                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"],
                                              }
                                    }},
                        {"$match": {"color_family": {"$exists": "false"}}},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {
                    "$unwind": "$sub_product"
                },
                {"$group": {
                    "_id": {
                        "color": "$sub_product.color_family",
                    },
                    "color": {
                        "$first": "$sub_product.color_family",
                    },
                    # "size_name": {
                    #     "$first": "$sub_product.product_size.size_Name"
                    # }
                }},
                # {"$match": {"$and": [
                #     {"color":  {"$exists": "false" }},]}},
                {
                    "$project": {
                        "_id": 0,
                        "color": 1,
                        # "size_name": 1,
                    }
                }

            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_price_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "priceFilter"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {
                    "$unwind": "$sub_product"
                },
                {"$group": {
                    "_id": "null",
                    "max_price": {"$max": "$sub_product.price"},
                    "min_price": {"$min": "$sub_product.price"}
                }},
                {
                    "$project": {
                        "_id": 0,
                        "min_price": 1,
                        "max_price": 1,
                        # "size_name": 1,
                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_occasion_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "occasion"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {"$lookup": {
                    "from": "occasion",
                    "localField": "occasion_id",
                    "foreignField": "occasion_id",
                    "as": "occasion"
                }},
                {
                    "$unwind": "$occasion"
                },
                {"$group": {
                    "_id": {
                        "color": "$occasion_id",
                    },
                    "occasion_id": {
                        "$first": "$occasion_id",
                    },
                    "occasion_name": {
                        "$first": "$occasion.occasion_Name"
                    }
                }},
                {
                    "$project": {
                        "_id": 0,
                        "occasion_id": 1,
                        "occasion_name": 1,
                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_sleeve_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "sleeve"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {"$lookup": {
                    "from": "sleeve_pattern",
                    "localField": "sleeve_Pattern_id",
                    "foreignField": "sleeve_pattern_id",
                    "as": "sleeve_pattern"
                }},
                {
                    "$unwind": "$sleeve_pattern"
                },
                {"$group": {
                    "_id": {
                        "color": "$sleeve_Pattern_id",
                    },
                    "sleeve_pattern_id": {
                        "$first": "$sleeve_Pattern_id",
                    },
                    "sleeve_pattern_name": {
                        "$first": "$sleeve_pattern.sleeve_pattern_Name"
                    }
                }},
                {
                    "$project": {
                        "_id": 0,
                        "sleeve_pattern_id": 1,
                        "sleeve_pattern_name": 1,
                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_neck_filter_list(request: Request, filter_data: get_product_list_model = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)
        filterType = "neck"
        queryResult = query_build(filterData, filterType, request)
        resultData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": queryResult["data"][0]["Query1"]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": queryResult["data"][0]["Query2"]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {"$lookup": {
                    "from": "neck_design",
                    "localField": "neck_design_id",
                    "foreignField": "neck_design_id",
                    "as": "neck_design"
                }},
                {
                    "$unwind": "$neck_design"
                },
                {"$group": {
                    "_id": {
                        "color": "$neck_design_id",
                    },
                    "neck_design_id": {
                        "$first": "$neck_design_id",
                    },
                    "neck_design_Name": {
                        "$first": "$neck_design.neck_design_Name"
                    }
                }},
                {
                    "$project": {
                        "_id": 0,
                        "neck_design_id": 1,
                        "neck_design_Name": 1,
                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_status_update(request: Request):
    response = {}
    try:
        last_date = (datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") + timedelta(days=-2)).strftime(
            "%Y-%m-%d")
        category_list = list(get_collection_order_details(request).aggregate(
            [{"$match": {"$expr": {'$and': [
                {"$eq": ["$delivery_status", 'shipped']},
                {"$lte": ["$ordered_date", last_date]}
            ]}}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details_id": 1,
                    }
                }
            ]))
        if len(category_list) > 0:
            updateSubProduct1 = get_collection_order_details(request).update_many(
                {"delivery_status": 'shipped', "ordered_date": {"$lte": last_date}},
                {"$set": {
                    "delivery_status": "received"
                }})

            array = [item["order_details_id"] for item in category_list]
            order_delivery_email_send(request, array)
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_delivery_email_send(request: Request, order_ids: List):
    response = {}
    try:
        currentDate = datetime.now().strftime("%b %d, %Y")
        for item in order_ids:
            category_list = list(get_collection_order_details(request).aggregate(
                [
                    {"$match": {'$and': [
                        {"order_details_id": item},

                    ]}},
                    {"$lookup": {
                        "from": "order",
                        "localField": "order_id",
                        "foreignField": "order_id",
                        "as": "order"
                    }},
                    {"$lookup": {
                        "from": "product",
                        "localField": "product_id",
                        "foreignField": "product_id",
                        "as": "product"
                    }},
                    {"$lookup": {
                        "from": "sub_product",
                        "localField": "sub_product_id",
                        "foreignField": "sub_product_id",
                        "pipeline": [
                            {"$lookup": {
                                "from": "product_size",
                                "localField": "size_id",
                                "foreignField": "size_id",
                                "as": "product_size"
                            }}
                        ],
                        "as": "sub_product"
                    }},
                    {"$lookup": {
                        "from": "users",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "users"
                    }},

                    {
                        "$project": {
                            "_id": {
                                "$toString": "$_id"
                            },
                            "order_details_id": 1,
                            "price": 1,
                            "total_price": 1,
                            "gst_price": 1,
                            "delivery_amount": 1,
                            "quantity": 1,
                            "track_id": 1,
                            "product.product_name": 1,
                            "sub_product.product_size.size_Name": 1,
                            "sub_product.images": 1,
                            "users.user_name": 1,
                            "users.email": 1,
                            "order.city": 1,
                            "order.country": 1,
                            "order.state": 1,
                            "order.pincode": 1,
                            "order.phone_number": 1,
                            "order.email": 1,
                            "order.street": 1,
                            "order.first_name": 1,
                            "order.last_name": 1,
                        }
                    }
                ]

            ))
            msg = MIMEMultipart()
            f = open(os.getcwd() + '/src/template/deliverytemplate.html', 'r')
            mail_content = f.read()
            p_image = Credantial.imageView + category_list[0]['sub_product'][0]['images'][0] if len(
                category_list[0]['sub_product']) > 0 and len(
                category_list[0]['sub_product'][0]['images']) > 0 else ''
            citySatate = category_list[0]["order"][0]['city'] + ", " + category_list[0]["order"][0]['city'] + "," if \
                category_list[0]["order"][0]['city'] != '' else ''
            address = category_list[0]["order"][0]['street'] + ',' + citySatate + ' ' + category_list[0]["order"][0][
                'pincode']
            name = category_list[0]["order"][0]['first_name'] + " " + category_list[0]["order"][0]['last_name']
            size = f"""
                  <span style="font-size:15px">Size <span style="font-weight: 600;">{category_list[0]["sub_product"][0]["product_size"][0]["size_Name"]} | </span></span>
    
    """ if len(category_list[0]["sub_product"]) > 0 and len(
                category_list[0]["sub_product"][0]['product_size']) > 0 else ''
            sizeQty = f"""<div>     {size}
                                                 <span style="font-size:15px"> Qty<span
                                                        style="font-weight: 600;"> {category_list[0]["quantity"]}</span></span>
    
                                            </div>"""

            mail_content = (mail_content.replace("##Name##", name).replace("##product_name##",
                                                                           category_list[0]['product'][0][
                                                                               "product_name"])
                            .replace('##orderId##', category_list[0]['order_details_id']).replace(' ##size_qty##',
                                                                                                  sizeQty).
                            replace(' ##address##', address).replace("#p_image", p_image))

            msg.attach(MIMEText(mail_content, 'html'))
            msg['Subject'] = 'Order Delivery Successfully'
            msg['From'] = Credantial.email_credential['email']
            msg['To'] = category_list[0]["order"][0]["email"]
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
                server.sendmail(Credantial.email_credential['email'], category_list[0]["order"][0]["email"],
                                msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_coupon_code_discount(request: Request, filter_data: coupon_code_request = Body(...)):
    response = {}
    try:
        filterData = jsonable_encoder(filter_data)

        product_ids = [o['product_id'] for o in filterData["check_out_list"]]
        print(product_ids)
        advertisementList = list(get_collection_advertisement(request).aggregate([
            {"$match": {"$and":[{"coupon_code": filterData["coupon_code"]},{"is_active":1},
                            {"is_delete":1}]}},
            {"$lookup": {
                "from": "product",
                # "localField": "product_id",
                # "foreignField": "product_id",
                "let": {"product": "$product_id","category":"$category_id","product_type":"$product_type_id",
                        "occasion":"$occasion_id","sleeve_Pattern":"$sleeve_Pattern_id","fabric_type":"$fabric_type_id",
                        "neck_design":"$neck_design_id","sub_Category":"$sub_Category_id","product_size":"$product_size_id"},
                "pipeline": [
        {"$match": {"$expr": {"$and": [
            {"$in": ["$product_id", product_ids]},
            {"$cond": {"if": {"$lte": [{"$size": "$$category"}, 0]}, "then":
                "true", "else": {"$in": [ "$category_id","$$category"]}, }},
            # {"$in": [ "$category_id","$$category"]},
            {"$cond": {"if": {"$lte": [{ "$size":"$$sub_Category"},0]}, "then":
                "true", "else": {"$in": ["$sub_Category_id", "$$sub_Category"]},}},
            # {"$in": ["$sub_Category_id", "$$sub_Category"]},
            {"$cond": {"if": {"$lte": [{ "$size":"$$product_type"},0]}, "then":
                "true", "else": {"$in": ["$product_type_id", "$$product_type"]},}},
            # {"$in": ["$product_type_id", "$$product_type"]},
            {"$cond": {"if": {"$lte": [{"$size": "$$occasion"}, 0]}, "then":
                "true", "else":    {"$in": ["$occasion_id", "$$occasion"]}, }},
            # {"$in": ["$occasion_id", "$$occasion"]},
            {"$cond": {"if": {"$lte": [{"$size": "$$sleeve_Pattern"}, 0]}, "then":
                "true", "else": {"$in": ["$sleeve_Pattern_id", "$$sleeve_Pattern"]}, }},
            # {"$in": ["$sleeve_Pattern_id", "$$sleeve_Pattern"]},
            {"$cond": {"if": {"$lte": [{"$size": "$$fabric_type"}, 0]}, "then":
                "true", "else": {"$in": ["$fabric_type_id", "$$fabric_type"]}, }},
            # {"$in": ["$fabric_type_id", "$$fabric_type"]},
            {"$cond": {"if": {"$lte": [{"$size": "$$neck_design"}, 0]}, "then":
                "true", "else": {"$in": ["$neck_design_id", "$$neck_design"]}, }},
            # {"$in": ["$neck_design_id", "$$neck_design"]}
            ] } }},
                    {"$lookup": {
                        "from": "sub_product",
                         # "localField": "sub_product_id",
                         # "foreignField": "sub_product_id",
                        "let": {"product": "$product_id"},
                     "pipeline": [
                        {"$match": {"$expr": {"$and": [
                        {"$eq": ["$product_id", "$$product"]},
                            {"$cond": {"if": {"$lte": [{"$size": "$$product_size"}, 0]}, "then":
                                "true", "else": {"$in": ["$size_id", "$$product_size"]}, }}
                        # {"$in": ["$size_id", "$$size"]}
                     ]}}}
                 ],
                "as": "sub_product"

                }}],
                "as": "product"
            }},
            {"$match": {
                "$expr": {"$gt": [
                    {"$size": "$product"},
                    0
                ]}
            }},
        {
            "$project": {
                "_id": {
                    "$toString": "$_id"
                },
                "product.product_id":1,
                "offer_percentage": 1,
                # "category_id":1,
                # "product.sub_product.sub_product_id":1,

            }
        }
    ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = advertisementList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

