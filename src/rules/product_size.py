from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.product_size import ProductSize, UpdateProductSize
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_product_size(request: Request):
    return request.app.database["product_size"]


def create_product_size(request: Request, product_size: ProductSize = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(product_size)
        value = insertData["size_Name"].lower()
        listData = list(get_collection_product_size(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$size_Name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_product_size(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "SIZE" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "SIZE" + '{:03}'.format(1)
            insertData[("size_id")] = customer_id
            new_addrs = get_collection_product_size(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Product Size Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Product Size is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_product_size(request: Request, id: str, Update_product_size: UpdateProductSize = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in Update_product_size.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("size_Name")
        if retVal is not None:
            value = update_data["size_Name"].lower()
            listData = list(get_collection_product_size(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$size_Name"
                        }, value]}},
                        {"size_id": {"$ne": id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_product_size(request).update_one({"size_id": id},
                                                                                {"$set": update_data})
                response["error_code"] = "9999"
                response["message"] = "Product Size Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Product Size is Exist"
        else:
            update_result = get_collection_product_size(request).update_one({"size_id": id},
                                                                            {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Product Size Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product_size_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)

        fabric_type_list = list(get_collection_product_size(request).aggregate(
            [{"$match": {"$and": [
                {"size_Name": {"$regex": users["search"], "$options": "i"}},
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
                        "size_Name": 1,
                        "size_id": 1,
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


def get_product_size_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_product_size(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "size_Name": 1,
                    "size_id": 1,
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
