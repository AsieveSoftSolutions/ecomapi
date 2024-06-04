from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.sub_category import SubCategory, UpdateSubCategory, MultipleUpdateSubCategory
from src.models.custom_model import response_return_model, get_user_model, get_sub_Category_model
from bson import ObjectId


def get_collection_sub_categroy(request: Request):
    return request.app.database["sub_category"]


def create_sub_category(request: Request, category: SubCategory = Body(...)):
    response = {}
    try:
        categorys = jsonable_encoder(category)
        value = categorys["sub_category_name"].lower()
        listData = list(get_collection_sub_categroy(request).aggregate(
            [{
                "$match": {
                    "$expr": {"$eq": [{
                        "$toLower": "$sub_category_name"
                    }, value]}
                }
            }]
        ))
        if len(listData) <= 0:
            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_sub_categroy(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "SUBCAT" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "SUBCAT" + '{:03}'.format(1)
            categorys["sub_Category_id"] = customer_id
            new_addrs = get_collection_sub_categroy(request).insert_one(categorys)
            response["error_code"] = "9999"
            response["message"] = "Sub Category Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Sub Category Name is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_sub_category_dropdown_list(request: Request):
    response = {}
    try:
        sub_Categorys = list(get_collection_sub_categroy(request).aggregate([
            {"$match": {"$and": [
                {"is_active": 1}
            ]}},
            {
                "$project": {

                    "_id": {
                        "$toString": "$_id"
                    },
                    "category_id": 1,
                    "sub_Category_id": 1,
                    "sub_category_name": 1,
                    "is_active": 1
                }
            }
        ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = sub_Categorys
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_sub_category(request: Request, updatesubCategory: MultipleUpdateSubCategory = Body(...)):
    response = {}
    try:
        catlist = jsonable_encoder(updatesubCategory)
        updateRecord = catlist["sub_category_list"]
        for item in updateRecord:
            update_result = get_collection_sub_categroy(request).update_one(
                {"sub_Category_id": item["sub_Category_id"]}, {"$set": item})
        response["error_code"] = "9999"
        response["message"] = "Sub Category Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_subCategory_name(request: Request, sub_cat_id: str, update_subcategory: UpdateSubCategory = Body(...)):
    response = {}
    try:
        subcategorys = {k: v for k, v in update_subcategory.dict().items() if v is not None}  # loop in the dict
        retVal = subcategorys.get("sub_category_name")
        if retVal is not None:
            value = subcategorys["sub_category_name"].lower()
            listData = list(get_collection_sub_categroy(request).aggregate(
                [{
                    "$match": {"$and": [{
                        "$expr": {"$eq": [{
                            "$toLower": "$sub_category_name"
                        }, value]}},
                        {"sub_Category_id": {"$ne": sub_cat_id},
                         }
                    ]}
                }]
            ))
            if len(listData) <= 0:
                update_result = get_collection_sub_categroy(request).update_one({"sub_Category_id": sub_cat_id},
                                                                                {"$set": subcategorys})
                response["error_code"] = "9999"
                response["message"] = "Sub Category Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Sub Category Name is Exist"
        else:
            update_result = get_collection_sub_categroy(request).update_one({"sub_Category_id": sub_cat_id},
                                                                            {"$set": subcategorys})
            response["error_code"] = "9999"
            response["message"] = "Sub Category Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_sub_category_list(request: Request, User: get_sub_Category_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(User)
        # Query = [ {"sub_category_name": {"$regex": users["search"], "$options": "i"}}]
        # if users["category_id"] !="0":
        #     Query.append({"category_id":users["category_id"]})
        subCategoryList = list(get_collection_sub_categroy(request).aggregate(
            [{"$match": {"$and": [
                {"sub_category_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["category_id"], "0"]}, "then":
                        {"$eq": [users["category_id"], "$category_id"]},
                              "else": "true"}}}
            ]}},
                {"$lookup": {
                    "from": "category",
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
                        "sub_Category_id": 1,
                        "sub_category_name": 1,
                        "is_active": 1,
                        "category.category_name": 1,

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
        response["data"] = subCategoryList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def delete_cart(request: Request, id: str):
    response = {}
    try:
        deleted_user = get_collection_sub_categroy(request).delete_one({"sub_Category_id": id})

        response["error_code"] = "9999"
        response["message"] = "Cart Delete Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
