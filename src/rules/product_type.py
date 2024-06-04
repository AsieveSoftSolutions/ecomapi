from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.product_type import ProductType, UpdateProductType
from src.models.custom_model import response_return_model, get_product_type_model
from bson import ObjectId


def get_collection_product_type(request: Request):
    return request.app.database["product_type"]
def get_collection_product(request: Request):
    return request.app.database["product"]

def create_product_type(request: Request, product_type: ProductType = Body(...)):
    response = {}
    try:
        productType = jsonable_encoder(product_type)
        value = productType["product_type_name"].lower()
        listData = []
        # listData = list(get_collection_product_type(request).aggregate(
        #   [{
        #     "$match": {
        #       "$expr": {"$eq": [{
        #         "$toLower": "$product_type_name"
        #       }, value]}
        #     }
        #   }]
        # ))
        if len(listData) <= 0:

            # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
            # if len(getuser) >0:
            customer_id = "CAT001"
            count = list(get_collection_product_type(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "PRODTYPE" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "PRODTYPE" + '{:03}'.format(1)
            productType["product_type_id"] = customer_id
            new_addrs = get_collection_product_type(request).insert_one(productType)
            response["error_code"] = "9999"
            response["message"] = "Product Type Add Successfully"
            # created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Product Type is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_product_type(request: Request, prod_type_id: str, update_ProductType: UpdateProductType = Body(...)):
    response = {}
    try:
        update_product_type = {k: v for k, v in update_ProductType.dict().items() if v is not None}  # loop in the dict
        retVal = update_product_type.get("product_type_name");
        if retVal is not None:
            value = update_product_type["product_type_name"].lower()
            listData = []
            isSubCategory = update_product_type.get("sub_Category_id")
            isCategory = update_product_type.get("category_id")
            # listData = list(get_collection_product_type(request).aggregate(
            #   [{
            #     "$match": {"$and": [{
            #       "$expr": {"$eq": [{
            #         "$toLower": "$product_type_name"
            #       }, value]}},
            #       {"product_type_id": {"$ne": prod_type_id}, }
            #     ]}
            #   }]
            # ))
            if isCategory is not None:
                getCategoryData = list(get_collection_product_type(request).aggregate(
                    [{"$match": {"$and": [{"product_type_id": prod_type_id},
                                          {"category_id": update_product_type["category_id"]}]}}]))
                if len(getCategoryData) <= 0:
                    updateSubProduct1 = get_collection_product(request).update_many(
                        {"product_type_id": prod_type_id},
                        {"$set": {
                            "category_id":update_product_type["category_id"]
                        }})
            if isSubCategory is not None:
                getCategoryData = list(get_collection_product_type(request).aggregate(
                    [{"$match": {"$and": [{"product_type_id": prod_type_id},
                                          {"sub_Category_id": update_product_type["sub_Category_id"]}]}}]))
                if len(getCategoryData) <= 0:
                    updateSubProduct1 = get_collection_product(request).update_many(
                        {"product_type_id": prod_type_id},
                        {"$set": {
                            "sub_Category_id": update_product_type["sub_Category_id"]
                        }})
            if len(listData) <= 0:
                update_result = get_collection_product_type(request).update_one({"product_type_id": prod_type_id},
                                                                                {"$set": update_product_type})
                response["error_code"] = "9999"
                response["message"] = "Product Type Update Successfully"
            else:
                response["error_code"] = "9998"
                response["message"] = "Already the Product Type is Exist"
        else:
            update_result = get_collection_product_type(request).update_one({"product_type_id": prod_type_id},
                                                                            {"$set": update_product_type})
            response["error_code"] = "9999"
            response["message"] = "Product Type Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product_type_list(request: Request, product_type: get_product_type_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(product_type)
        # Query = [{"product_type_name": {"$regex": users["search"], "$options": "i"}}]
        # if users["category_id"] != "0":
        #   Query.append({"category_id": users["category_id"]})
        # if users["sub_Category_id"] != "0":
        #   Query.append({"sub_Category_id": users["sub_Category_id"]})

        productTypeList = list(get_collection_product_type(request).aggregate(
            [{"$match": {"$and": [
                {"product_type_name": {"$regex": users["search"], "$options": "i"}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["is_active"], 2]}, "then":
                        {"$eq": [users["is_active"], "$is_active"]},
                              "else": "true"}}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["category_id"], "0"]}, "then":
                        {"$eq": [users["category_id"], "$category_id"]},
                              "else": "true"}}},
                {"$expr": {
                    "$cond": {"if": {"$ne": [users["sub_Category_id"], "0"]}, "then":
                        {"$eq": [users["sub_Category_id"], "$sub_Category_id"]},
                              "else": "true"}}}
            ]}},
                {"$lookup": {
                    "from": "category",
                    "localField": "category_id",
                    "foreignField": "category_id",
                    "as": "category"}},
                {"$lookup": {
                    "from": "sub_category",
                    "localField": "sub_Category_id",
                    "foreignField": "sub_Category_id",
                    "as": "sub_category"}},
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
                        "product_type_name": 1,
                        "product_type_id": 1,
                        "is_active": 1,
                        "image": 1,
                        "category.category_name": 1,
                        "sub_category.sub_category_name": 1,

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
        response["data"] = productTypeList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product_type_dropdown_list(request: Request):
    response = {}
    try:
        getdata = list(get_collection_product_type(request).aggregate([
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
                    "product_type_name": 1,
                    "product_type_id": 1,
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
