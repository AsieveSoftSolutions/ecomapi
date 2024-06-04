from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.sleeve_pattern import SleevePattern, UpdateSleevePattern
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_sleeve_pattern(request: Request):
    return request.app.database["sleeve_pattern"]


def create_sleeve_pattern(request: Request, sleeve_pattern: SleevePattern = Body(...)):
    response = {}
    try:
        sleevePattern = jsonable_encoder(sleeve_pattern)
        value = sleevePattern["sleeve_pattern_Name"].lower()
        listData = list(get_collection_sleeve_pattern(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$sleeve_pattern_Name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_sleeve_pattern(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "SLVPTN" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "SLVPTN" + '{:03}'.format(1)
            sleevePattern[("sleeve_pattern_id")] = customer_id
            new_addrs = get_collection_sleeve_pattern(request).insert_one(sleevePattern)
            response["error_code"] = "9999"
            response["message"] = "Sleeve Pattern Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Sleeve Pattern is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_sleeve_pattern(request: Request, slv_ptn_id: str, update_sleevePattern: UpdateSleevePattern = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in update_sleevePattern.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("sleeve_pattern_Name")
        if retVal is not None:
            value = update_data["sleeve_pattern_Name"].lower()
            listData = list(get_collection_sleeve_pattern(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$sleeve_pattern_Name"
                        }, value]}},
                        {"sleeve_pattern_id": {"$ne": slv_ptn_id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_sleeve_pattern(request).update_one({"sleeve_pattern_id": slv_ptn_id},
                                                                                  {"$set": update_data})
                response["error_code"] = "9999"
                response["message"] = "Sleeve Pattern Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Sleeve Pattern is Exist"
        else:
            update_result = get_collection_sleeve_pattern(request).update_one({"sleeve_pattern_id": slv_ptn_id},
                                                                              {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Sleeve Pattern Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_sleeve_pattern_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_sleeve_pattern(request).aggregate(
            [{"$match": {"$and": [
                {"sleeve_pattern_Name": {"$regex": users["search"], "$options": "i"}},
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
                        "sleeve_pattern_Name": 1,
                        "sleeve_pattern_id": 1,
                        "is_active": 1,
                    }
                } , {
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


def get_sleeve_pattern_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_sleeve_pattern(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "sleeve_pattern_Name": 1,
                    "sleeve_pattern_id": 1,
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
