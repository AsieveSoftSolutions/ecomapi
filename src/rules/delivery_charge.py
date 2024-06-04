from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.delivery_charge import DeliveryCharge, UpdateDeliveryCharge
from src.models.custom_model import response_return_model, get_user_model,get_user_delivery_request
from bson import ObjectId


def get_collection_deliver_charge(request: Request):
    return request.app.database["delivery_charge"]


def create_delivery_charge(request: Request, occasion: DeliveryCharge = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(occasion)

        listData = list(get_collection_deliver_charge(request).aggregate(
            [{
                "$match": {"$and": [{"postal_service_id": insertData["postal_service_id"]},
                                    {"types": insertData["types"]},
                                    {"kg": insertData["kg"]}
                                    ]}
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_deliver_charge(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "DC" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "DC" + '{:03}'.format(1)
            insertData["delivery_charge_id"] = customer_id
            new_addrs = get_collection_deliver_charge(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Delivery Charge Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Delivery Charge is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_delivery_charge(request: Request, id: str, update_occasion: UpdateDeliveryCharge = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in update_occasion.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("postal_service_id")
        if retVal is not None:

            listData = list(get_collection_deliver_charge(request).aggregate(
                [{
                    "$match": {"$and": [
                        {"delivery_charge_id": {"$ne": id}},
                        {"postal_service_id": update_data["postal_service_id"]},
                        {"types": update_data["types"]},
                        {"kg": update_data["kg"]}
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_deliver_charge(request).update_one({"delivery_charge_id": id},
                                                                                  {"$set": update_data})
                response["error_code"] = "9999"
                response["message"] = "Delivery Charge Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Delivery Charge is Exist"
        else:
            update_result = get_collection_deliver_charge(request).update_one({"delivery_charge_id": id},
                                                                              {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Delivery Charge Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_delivery_charge_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_deliver_charge(request).aggregate(
            [{"$match": {"$and": [
                # {"tax_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["postal_id"], '']}, "then":
                        {"$eq": [users["postal_id"], "$postal_service_id"]},
                              "else": "true"}}}
            ]}},
                {"$lookup": {
                    "from": "postal_service",
                    # "localField": "postal_service_id",
                    # "foreignField": "postal_service_id",
                    "let": {"postal_service_id": "$postal_service_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [{"$eq": ["$postal_service_id", "$$postal_service_id"]},
                                                       {
                                                           "$cond": {"if": {"$ne": [users["country"], '']}, "then":
                                                               {"$eq": [users["country"], "$country"]},
                                                                     "else": "true"}}]
                                              }
                                    }},
                    ],
                    "as": "postal_service"
                }},
                {"$match": {
                    "$expr": {"$gt": [
                        {"$size": "$postal_service"},
                        0]}
                }},
                {
                    "$sort": {"kg": 1}
                },
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
                        "postal_service_id": 1,
                        "delivery_charge_id": 1,
                        "kg":1,
                        "types":1,
                        "delivery_charge": 1,
                        "is_active": 1,
                        "postal_service.country":1,
                        "postal_service.postal_service_name": 1,
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


def get_delivery_charge_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_deliver_charge(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "postal_service_id": 1,
                    "delivery_charge_id": 1,
                    "kg": 1,
                    "types": 1,
                    "delivery_charge": 1,
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

def get_user_delivery_charge(request: Request, user: get_user_delivery_request = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)
        getDataList = list(get_collection_deliver_charge(request).aggregate(
            [{"$match": {"$and": [
                 {"postal_service_id": users["postal_id"]},
                {"$expr": {
                    "$cond": {"if": {"$ne": ["$types", "normal"]}, "then":
                        {"$gte": ["$kg", users["weight"]]},
                              "else": "true"}}}
            ]}},

                # {
                #     "$skip": users["skip_count"]
                # },
                {
                    "$limit": 1
                },
                {
                    "$project": {
                        "_id": 0,
                        "delivery_charge": 1,

                    }
                }
            ]))
        if(len(getDataList) ==0 ):
            getDataList = list(get_collection_deliver_charge(request).aggregate(
            [{"$match": {"$and": [
                 {"postal_service_id": users["postal_id"]},
                {"$expr": {
                    "$cond": {"if": {"$ne": ["$types", "normal"]}, "then":
                        {"$lte": ["$kg", users["weight"]]},
                              "else": "true"}}}
            ]}},
                {
                    "$sort": {"kg": -1}
                },

                # {
                #     "$skip": users["skip_count"]
                # },
                {
                    "$limit": 1
                },
                {
                    "$project": {
                        "_id": 0,
                        "delivery_charge": 1,

                    }
                }
            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = getDataList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response