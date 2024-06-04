from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.postal_service import PostalService, UpdatePostalService
from src.models.custom_model import response_return_model, get_user_model, get_user_postal_request
from bson import ObjectId


def get_collection_postal_service(request: Request):
    return request.app.database["postal_service"]


def create_postal_service(request: Request, occasion: PostalService = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(occasion)
        value = insertData["postal_service_name"].lower()
        listData = list(get_collection_postal_service(request).aggregate(
            [{
                "$match": {"$and": [{
                    "$expr": {"$eq": [{
                        "$toLower": "$postal_service_name"
                    }, value]}},
                    {"country": {"$eq": insertData['country']}}
                ]}
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_postal_service(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "POST" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "POST" + '{:03}'.format(1)
            insertData["postal_service_id"] = customer_id
            new_addrs = get_collection_postal_service(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Postal Service Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Postal Service is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_postal_service(request: Request, id: str, update_occasion: UpdatePostalService = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in update_occasion.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("occasion_Name")
        if retVal is not None:
            value = update_data["postal_service_name"].lower()
            listData = list(get_collection_postal_service(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$postal_service_name"
                        }, value]}},
                        {"postal_service_id": {"$ne": id}, },
                        {"country": {"$eq": update_data['country']}}
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_postal_service(request).update_one({"postal_service_id": id},
                                                                                  {"$set": update_data})
                response["error_code"] = "9999"
                response["message"] = "Postal Service Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Postal Service is Exist"
        else:
            update_result = get_collection_postal_service(request).update_one({"postal_service_id": id},
                                                                              {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Postal Service Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_postal_service_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_postal_service(request).aggregate(
            [{"$match": {"$and": [
                {"postal_service_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}}
            ]}},
                # {
                #     "$skip": users["skip_count"]
                # },
                # {
                #     "$limit": users["limit"]
                # },
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "postal_service_name": 1,
                        "postal_service_id": 1,
                        "url": 1,
                        "country": 1,
                        "is_active": 1,
                    }
                }, {
                "$facet": {
                    "data": [
                        {'$skip': users["skip_count"]},
                        {"$limit": users["limit"]}
                    ],
                    "pagination": [
                        {"$count": "total"}
                    ]
                }
            }

            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = fabric_type_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_postal_service_dropdown_list(request: Request):
    response = {}
    try:

        getdata = list(get_collection_postal_service(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},

            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "postal_service_name": 1,
                    "postal_service_id": 1,
                    "country": 1,
                    "url": 1,
                    "is_active": 1,
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = getdata
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_user_postal_service_list(request: Request, user: get_user_postal_request = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)
        getdata = list(get_collection_postal_service(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1},
                {"country": users["country"]}
            ]}},
            {"$lookup": {
                "from": "delivery_charge",
                # "localField": "postal_service_id",
                # "foreignField": "postal_service_id",
                "let": {"postal_service_id": "$postal_service_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$and": [{"$eq": ["$postal_service_id", "$$postal_service_id"]},
                                                   {"$eq": ["$is_active", 1]}]
                                          }
                                }},
                ],
                "as": "delivery_charge"
            }},
            {"$match": {
                "$expr": {"$gt": [
                    {"$size": "$delivery_charge"},
                    0] }
            }},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "postal_service_name": 1,
                    "postal_service_id": 1,
                    "country": 1,
                    "url": 1,
                    "is_active": 1,
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = getdata
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_country_list(request: Request, types: int):
    response = {}
    try:

        getdata = list(get_collection_postal_service(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {"$lookup": {
                "from": "delivery_charge",
                # "localField": "postal_service_id",
                # "foreignField": "postal_service_id",
                "let": {"postal_service_id": "$postal_service_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$and": [{"$eq": ["$postal_service_id", "$$postal_service_id"]},
                                                   {"$eq": ["$is_active", 1]}]
                                          }
                                }},
                ],
                "as": "delivery_charge"
            }},
            {"$match": {
                "$expr": {"$cond": {"if": {"$eq": [types, 1]}, "then":
                    "true", "else": {"$gt": [
                    {"$size": "$delivery_charge"},
                    0]}}
                          }
            }},
            {"$group": {
                "_id": {
                    "country": "$country",
                },
                "country": {
                    "$first": "$country",
                }}},
            {
                "$project": {

                    "_id": 0,
                    "country": 1,
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = getdata
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
