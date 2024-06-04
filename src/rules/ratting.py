from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.ratting import Ratting, UpdateRatting
from src.models.custom_model import response_return_model, get_user_model, get_ratting_model, get_ratting_list_request
from bson import ObjectId
import uuid
from typing import List


def get_collection_ratting(request: Request):
    return request.app.database["ratting"]


def get_collection_product(request: Request):
    return request.app.database["product"]


def create_ratting(request: Request, ratting: Ratting = Body(...)):
    response = {}
    try:

        insertData = jsonable_encoder(ratting)
        cartData = list(get_collection_ratting(request).aggregate(
            [{"$match": {"$and": [{"product_id": insertData["product_id"]},
                                  {"user_id": insertData["user_id"]}]}}]))
        if len(cartData) <= 0:
            insertData["ratting_id"] = "RATTING-" + str(uuid.uuid4()).replace('-', '')
            insert = get_collection_ratting(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Ratting Add Successfully"
        else:
            response["error_code"] = "9999"
            response["message"] = "Ratting Add Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_ratting(request: Request, id: str, update_ratting: UpdateRatting = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in update_ratting.dict().items() if v is not None}  # loop in the dict
        update_result = get_collection_ratting(request).update_one({"ratting_id": id}, {"$set": updateData})
        response["error_code"] = "9999"
        response["message"] = "Ratting Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_rating_list(request: Request, ratting_model: get_ratting_model = Body(...)):
    response = {}
    try:

        getData = jsonable_encoder(ratting_model)
        limitCount = getData["limit"]
        if getData["limit"] == 0:
            limitList = list(get_collection_ratting(request).aggregate(
                [{"$match": {"$and": [{"product_id": getData["product_id"]}]}},
                 {"$count": "myCount"}]))
            limitCount = limitList[0]["myCount"]

        rattingList = list(get_collection_ratting(request).aggregate(
            [{"$match": {"$and": [{"product_id": getData["product_id"]}]}},

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
                     "feedback": 1,
                     "ratting_value": 1,
                     "users.user_name": 1,
                     "users.profile": 1,

                 }
             },
             {
                 "$facet": {
                     "data": [
                         {"$limit": limitCount}
                     ],
                     "pagination": [
                         {"$count": "total"}
                     ]
                 }
             },
             # {
             #     "$addFields": {
             #         "totalCount" : {"$count": "myCount"}
             #     }
             # },
             # {"$limit": limitCount},

             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = rattingList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_all_product_rating_list(request, ratting_model):
    response = {}
    try:
        getData = jsonable_encoder(ratting_model)
        productData = []
        productArray = []
        if getData["search"] != "":
            productData = list(get_collection_product(request).aggregate([
                {"$match": {"$and": [{"is_active": 1},
                                     {"product_name": {"$regex": getData["search"], "$options": "i"}}]}}, {
                    "$project": {
                        "product_id": 1,
                        "_id": 0,
                    }
                }
            ]))
            # productArray.append([o[0].product_id for o in productData])
            # print(productArray)
        rattingList = list(get_collection_ratting(request).aggregate(
            [{"$match": {"$and": [{"is_active": 1},
                                  # {"$expr": {
                                  #     "$cond": {"if": {"$ne": [getData["search"], ""]}, "then":
                                  #         {"$lte": [advertisementList[0]["validate_from"], "$created_date"]},
                                  #               "else": "true"}}},
                                  ]}},
             {"$lookup": {
                 "from": "product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}, ]}}},
                     # {"$lookup": {
                     #     "from": "product_size",
                     #     "localField": "size_id",
                     #     "foreignField": "size_id",
                     #     "as": "product_size"
                     # }}
                 ],
                 "as": "product"
             }},
             {"$group": {
                 "_id": {
                     "product_id": "$product_id",
                 },
                 "product_id": {
                     "$first": "$product_id",
                 },
                 "count": {
                     "$sum": 1
                 },
                 "total": {
                     "$sum": "$ratting_value"
                 },
                 "product_name": {
                     "$first": "$product.product_name"
                 }
             }},
             {
                 "$project": {
                     "_id": 0,
                     "count": 1,
                     "total": 1,
                     "product_id": 1,
                     "product_name": 1,
                     "rattingTotal": {
                         "$cond":
                             {
                                 "if": {
                                     "$ne": [
                                         "$count",
                                         0
                                     ]
                                 }, "then":
                                 {"$divide": ["$total", "$count"]},
                                 "else": 0
                             }},
                 }
             },
             {
                 "$facet": {
                     "data": [
                         {'$skip': getData["skip_count"]},
                         {"$limit": getData["limit"]}
                     ],
                     "pagination": [
                         {"$count": "total"}
                     ]
                 }
             },
             ]
        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = rattingList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product_rating_list(request: Request, ratting_model: get_ratting_list_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(ratting_model)

        rattingList = list(get_collection_ratting(request).aggregate([
            {"$match": {"$and": [{"product_id": getData["product_id"]},
                                 {"$expr": {
                                     "$cond": {"if": {"$ne": [getData["type"], 2]}, "then":
                                         {"$eq": ["$is_active", 1]},
                                               "else": "true"}}},
                                 {"$expr": {
                                     "$cond": {"if": {"$ne": [getData["rating_range"], 0]}, "then":
                                         {"$eq": [getData["rating_range"], "$ratting_value"]},
                                               "else": "true"}}},
                                 # {"ratting_value": {"$": getData["rating_range"]}}
                                 ]}},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "users"
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
                    }}],

                "as": "sub_product"}},
            {
                "$sort": {"updated_date": -1}
            },
            # { "$group": {"_id": "null", "totalRatting": { "$sum": "$ratting_value"}}},
            # {"$addFields": {"totalRatting": {"$sum": "$ratting_value"},
            #                 }},
            {
                "$project": {
                    "_id": {
                        "$toString": "$_id"
                    },
                    "feedback": 1,
                    "ratting_id":1,
                    "ratting_value": 1,
                    "users.user_name": 1,
                    "users.profile": 1,
                    "sub_product.product_size.size_Name": 1,
                    "sub_product.color": 1,
                    "image":1,
                    "is_active":1,
                    # "totalRatting": 1,

                }
            },
            {
                "$facet": {
                    "data": [
                        # {'$skip': getData["skip"]},
                        {"$limit": getData["limit"]}
                    ],
                    "pagination": [
                        {"$count": "total"}
                    ]
                }
            },
        ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = rattingList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
