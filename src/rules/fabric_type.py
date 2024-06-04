from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.fabric_type import FabricType, UpdateFabricType
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_fabric_type(request: Request):
    return request.app.database["fabric_type"]


def create_fabric_type(request: Request, fabric_type: FabricType = Body(...)):
    response = {}
    try:
        fabricType = jsonable_encoder(fabric_type)
        value = fabricType["fabric_name"].lower()
        listData = list(get_collection_fabric_type(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$fabric_name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_fabric_type(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "FABTYPE" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "FABTYPE" + '{:03}'.format(1)
            fabricType["fabric_id"] = customer_id
            new_addrs = get_collection_fabric_type(request).insert_one(fabricType)
            response["error_code"] = "9999"
            response["message"] = "Fabric Type Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Fabric is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_fabric_type(request: Request, fab_type_id: str, update_fabricType: UpdateFabricType = Body(...)):
    response = {}
    try:
        update_fabric_type = {k: v for k, v in update_fabricType.dict().items() if v is not None}  # loop in the dict
        retVal = update_fabric_type.get("fabric_name")
        if retVal is not None:
            value = update_fabric_type["fabric_name"].lower()
            listData = list(get_collection_fabric_type(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$fabric_name"
                        }, value]}},
                        {"fabric_id": {"$ne": fab_type_id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_fabric_type(request).update_one({"fabric_id": fab_type_id},
                                                                               {"$set": update_fabric_type})
                response["error_code"] = "9999"
                response["message"] = "Fabric Type Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Fabric is Exist"
        else:
            update_result = get_collection_fabric_type(request).update_one({"fabric_id": fab_type_id},
                                                                           {"$set": update_fabric_type})
            response["error_code"] = "9999"
            response["message"] = "Fabric Type Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_fabric_type_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_fabric_type(request).aggregate(
            [{"$match": {"$and": [
                {"fabric_name": {"$regex": users["search"], "$options": "i"}},
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
                        "fabric_id": 1,
                        "fabric_name": 1,
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


def get_fabric_type_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_fabric_type(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "fabric_id": 1,
                    "fabric_name": 1,
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
