from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.brand import Brand, UpdateBrand
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_brand(request: Request):
    return request.app.database["brand"]


def create_brand(request: Request, brand: Brand = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(brand)
        value = insertData["brand_name"].lower()
        listData = list(get_collection_brand(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$brand_name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_brand(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "BRAND" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "BRAND" + '{:03}'.format(1)
            insertData["brand_id"] = customer_id
            new_addrs = get_collection_brand(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Brand Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Brand is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_brand(request: Request, id: str, brand: UpdateBrand = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in brand.dict().items() if v is not None}  # loop in the dict
        retVal = updateData.get("brand_name")
        if retVal is not None:
            value = updateData["brand_name"].lower()
            listData = list(get_collection_brand(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$brand_name"
                        }, value]}},
                        {"fabric_id": {"$ne": id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_brand(request).update_one({"brand_id": id},
                                                                               {"$set": updateData})
                response["error_code"] = "9999"
                response["message"] = "Brand Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Brand is Exist"
        else:
            update_result = get_collection_brand(request).update_one({"brand_id": id},
                                                                           {"$set": updateData})
            response["error_code"] = "9999"
            response["message"] = "Brand Type Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_brand_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_brand(request).aggregate(
            [{"$match": {"$and": [
                {"brand_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}}

            ]}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "brand_id": 1,
                        "brand_name": 1,
                        "is_active": 1,
                    }
                },
                {
                    "$facet": {
                        "data": [
                            {'$skip': users["skip_count"]},
                            {"$limit": users["limit"]}
                        ],
                        "pagination": [
                            {"$count": "total"}
                        ]
                    }
                },

            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = fabric_type_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_brand_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_brand(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "brand_id": 1,
                    "brand_name": 1,
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
