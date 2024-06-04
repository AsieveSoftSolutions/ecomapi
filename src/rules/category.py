from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.category import Category, UpdateCategory
from src.models.custom_model import response_return_model, get_user_model
from bson import ObjectId


def get_collection_categroy(request: Request):
    return request.app.database["category"]


def create_category(request: Request, category: Category = Body(...)):
    response = {}
    try:
        categorys = jsonable_encoder(category)
        value = categorys["category_name"].lower()
        categroyDate = list(get_collection_categroy(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$category_name"
                    }, value]}
                }
            }]
        ))
        if len(categroyDate) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_categroy(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "CAT" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "CAT" + '{:03}'.format(1)
            categorys["category_id"] = customer_id
            new_addrs = get_collection_categroy(request).insert_one(categorys)
            response["error_code"] = "9999"
            response["message"] = "Category Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Category is Exist"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_category_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)
        category_list = list(get_collection_categroy(request).aggregate(
            [{"$match": {"$and": [
                {"category_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}}
            ]}}
                ,
                {"$lookup": {
                    "from": "sub_category",
                    "localField": "category_id",
                    "foreignField": "category_id",
                    "as": "category"}},
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
                        "category_id": 1,
                        "category_name": 1,
                        "is_active": 1,
                        "category.sub_category_name": 1,

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
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_category(request: Request, id: str, category: UpdateCategory = Body(...)):
    response = {}
    try:
        categorys = {k: v for k, v in category.dict().items() if v is not None}  # loop in the dict
        retVal = categorys.get("category_name")
        if retVal is not None:
            value = categorys["category_name"].lower()
            listData = list(get_collection_categroy(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$category_name"
                        }, value]}},
                        {"category_id": {"$ne": id}, }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_categroy(request).update_one({"category_id": id}, {"$set": categorys})
                response["error_code"] = "9999"
                response["message"] = "Category Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Category is Exist"
        else:
            update_result = get_collection_categroy(request).update_one({"category_id": id}, {"$set": categorys})
            response["error_code"] = "9999"
            response["message"] = "Category Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_dropdown_category_list(request: Request):
    response = {}
    try:
        category_list = list(get_collection_categroy(request).aggregate(
            [{"$match":
                  {"is_active": 1}},

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
        # category_list
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
