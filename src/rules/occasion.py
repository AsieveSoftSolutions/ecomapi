from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.occasion import Occasion, UpdateOccasion
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_occasion(request: Request):
    return request.app.database["occasion"]


def create_occasion(request: Request, occasion: Occasion = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(occasion)
        value = insertData["occasion_Name"].lower()
        listData = list(get_collection_occasion(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$occasion_Name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_occasion(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "OCC" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "OCC" + '{:03}'.format(1)
            insertData[("occasion_id")] = customer_id
            new_addrs = get_collection_occasion(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Occasion Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Occasion is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_occasion(request: Request, id: str, update_occasion: UpdateOccasion = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in update_occasion.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("occasion_Name")
        if retVal is not None:
            value = update_data["occasion_Name"].lower()
            listData = list(get_collection_occasion(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$occasion_Name"
                        }, value]}},
                        {"occasion_id": {"$ne": id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_occasion(request).update_one({"occasion_id": id},
                                                                            {"$set": update_data})
                response["error_code"] = "9999"
                response["message"] = "Occasion Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Occasion is Exist"
        else:
            update_result = get_collection_occasion(request).update_one({"occasion_id": id},
                                                                        {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Occasion Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_occasion_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_occasion(request).aggregate(
            [{"$match": {"$and": [
                {"occasion_Name": {"$regex": users["search"], "$options": "i"}},
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
                        "occasion_Name": 1,
                        "occasion_id": 1,
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


def get_occasion_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_occasion(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "occasion_Name": 1,
                    "occasion_id": 1,
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
