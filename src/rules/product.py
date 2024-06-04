from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.product import Product, UpdateProduct
from src.models.custom_model import response_return_model, get_user_model, get_product_model, get_product_list_model, \
    get_product_details_model
from bson import ObjectId
from typing import List
from src.models.sub_product import UpdateSubProduct, SubProductList


def get_collection_product(request: Request):
    return request.app.database["product"]


def get_collection_sub_product(request: Request):
    return request.app.database["sub_product"]


def get_collection_advertisement(request: Request):
    return request.app.database["advertisement"]


def create_product(request: Request, product: Product = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(product)
        productData = jsonable_encoder(product)
        del productData['sub_product']

        value = productData["product_name"].lower()
        listData = []
        # listData = list(get_collection_product(request).aggregate(
        #     [{
        #         "$match": {
        #             "$expr": {"$eq": [{
        #                 "$toLower": "$product_name"
        #             }, value]}
        #         }
        #     }]
        # ))
        if len(listData) <= 0:
            product_id = "CAT001"
            count = list(get_collection_product(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                product_id = "PROD" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                product_id = "PROD" + '{:03}'.format(1)
            productData["product_id"] = product_id
            insertproduct = get_collection_product(request).insert_one(productData)
            for item in insertData['sub_product']:
                item["product_id"] = product_id
                sub_product_id = "CAT001"
                subcount = list(get_collection_sub_product(request).aggregate([{"$count": "myCount"}]))
                if len(subcount) != 0:
                    sub_product_id = "SUBPROD" + '{:03}'.format(subcount[0]["myCount"] + 1)
                else:
                    sub_product_id = "SUBPROD" + '{:03}'.format(1)
                item["sub_product_id"] = sub_product_id
                insertSubProduct = get_collection_sub_product(request).insert_one(item)
            response["error_code"] = "9999"
            response["message"] = "Product Add Successfully"

        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Product is Exist"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_product(request: Request, id: str, update_product: UpdateProduct = Body(...)):
    response = {}
    try:
        updateData = jsonable_encoder(update_product)
        productData = jsonable_encoder(update_product)
        del productData['sub_product']
        value = productData["product_name"].lower()
        listData = []
        # listData = list(get_collection_product(request).aggregate(
        #     [{
        #         "$match": {"$and": [{
        #             "$expr": {"$eq": [{
        #                 "$toLower": "$product_name"
        #             }, value]}},
        #             {"product_id": {"$ne": id}, }
        #         ]}
        #     }]
        # ))
        if len(listData) <= 0:
            update_result = get_collection_product(request).update_one({"product_id": id},
                                                                       {"$set": productData})
            for item in updateData['sub_product']:

                sub_product_data = list(get_collection_sub_product(request).aggregate([
                    {"$match": {"$and": [{"product_id": id}, {"size_id": item["size_id"]},
                                         {"color": item["color"]}]}}]))
                if len(sub_product_data) <= 0:
                    item["product_id"] = id
                    sub_product_id = "CAT001"
                    count = list(get_collection_sub_product(request).aggregate([{"$count": "myCount"}]))
                    sub_product_id = "SUBPROD" + '{:03}'.format(count[0]["myCount"] + 1)
                    item["sub_product_id"] = sub_product_id
                    insertSubProduct = get_collection_sub_product(request).insert_one(item)
                else:
                    item["total_quantity"] = item["total_quantity"] + sub_product_data[0]["total_quantity"]
                    updateSubProduct = get_collection_sub_product(request).update_one(
                        {"sub_product_id": sub_product_data[0]["sub_product_id"]},
                        {"$set": item})
            response["error_code"] = "9999"
            response["message"] = "Product Update Successfully"
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Product is Exist"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product_list(request: Request, productModel: get_product_model = Body(...)):
    response = {}
    try:
        getProduct = jsonable_encoder(productModel)
        Query = [{'is_delete':1},{"product_name": {"$regex": getProduct["search"], "$options": "i"}}]
        if getProduct["category_id"] != "0":
            Query.append({"category_id": getProduct["category_id"]})
        if getProduct["sub_Category_id"] != "0":
            Query.append({"sub_Category_id": getProduct["sub_Category_id"]})
        if getProduct["product_type_id"] != "0":
            Query.append({"product_type_id": getProduct["product_type_id"]})
        productList = list(get_collection_product(request).aggregate(
            [{"$match": {"$and": Query}},
             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ['$is_delete', 1]},
                                                    {"$eq": ["$product_id", "$$product"]}]
                                           }
                                 }},
                     {"$lookup": {
                         "from": "product_size",
                         "localField": "size_id",
                         "foreignField": "size_id",
                         "as": "product_size"
                     }}],

                 "as": "sub_product"}},
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
             {"$lookup": {
                 "from": "product_type",
                 "localField": "product_type_id",
                 "foreignField": "product_type_id",
                 "as": "product_type"}},
             {
                 "$sort": {"created_date": -1}
             },
             # {
             #     "$skip": getProduct["skip_count"]
             # },
             # {
             #     "$limit": getProduct["limit"]
             # },
             {
                 "$addFields": {
                     "available_quantity": {"$sum": "$sub_product.quantity"},
                     "overall_quantity": {"$sum": "$sub_product.total_quantity"}
                 }
             },
             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "category_id": 1,
                     "sub_Category_id": 1,
                     "product_type_id": 1,
                     "product_name": 1,
                     "product_id": 1,
                     "is_active": 1,
                     "occasion_id": 1,
                     "sleeve_Pattern_id": 1,
                     "fabric_type_id": 1,
                     "neck_design_id": 1,
                     "dress_length": 1,
                     "dress_weight": 1,
                     "fitting": 1,
                     "product_url": 1,
                     "no_size": 1,
                     "description": 1,
                     "size_chart_image": 1,
                     "category.category_name": 1,
                     "sub_category.sub_category_name": 1,
                     "product_type.product_type_name": 1,
                     "sub_product.sub_product_id": 1,
                     "sub_product.product_size.size_Name": 1,
                     "sub_product.size_id": 1,
                     "sub_product.color": 1,
                     "sub_product.images": 1,
                     "sub_product.price": 1,
                     "sub_product.quantity": 1,
                     "sub_product.total_quantity": 1,
                     "sub_product.cost_per_item": 1,
                     "sub_product.profit": 1,
                     "sub_product.margin": 1,
                     "sub_product.expense": 1,
                     "available_quantity": 1,
                     "overall_quantity":1,
                 }
             },{
                    "$facet": {
                        "data": [
                            {'$skip': getProduct["skip_count"]},
                            {"$limit": getProduct["limit"]}
                        ],
                        "pagination": [
                            {"$count": "total"}
                        ]
                    }
                }

             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = productList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def  get_product_user_list(request: Request, productListModel: get_product_list_model = Body(...)):
    response = {}
    try:
        getProduct = jsonable_encoder(productListModel)

        advertisementList = []
        if getProduct["advertisement_id"] != "":
            advertisementList = list(get_collection_advertisement(request).aggregate([
                {"$match": {"advertisement_id": getProduct["advertisement_id"]}},
                {
                    "$project": {
                        "_id": {"$toString": "$_id"},
                        "coupon_code": 1,
                        "offer_percentage": 1,
                        "advertisement_name": 1,
                        "category_id": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "product_size_id": 1,
                        "validate_from": 1,
                        "validate_to": 1,
                        "product_from": 1,
                        "product_to": 1,
                    }
                }
            ]))
        else:
            advertisement = {}
            advertisement["product_from"] = ""
            advertisement["product_to"] = ""
            advertisementList.append(advertisement)

        retVal = advertisementList[0].get("sleeve_Pattern_id")
        if retVal is not None:
            getProduct["sleeve_pattern"] = getProduct["sleeve_pattern"] + advertisementList[0]["sleeve_Pattern_id"]
            getProduct["product_type"] = getProduct["product_type"] + advertisementList[0]["product_type_id"]
            getProduct["category"] = getProduct["category"] + advertisementList[0]["category_id"]
            getProduct["fabric_type"] = getProduct["fabric_type"] + advertisementList[0]["fabric_type_id"]
            getProduct["occasion"] = getProduct["occasion"] + advertisementList[0]["occasion_id"]
            getProduct["neck_design"] = getProduct["neck_design"] + advertisementList[0]["neck_design_id"]
            if getProduct["sub_category"] is not None:
                getProduct["sub_category"] = getProduct["sub_category"] + advertisementList[0]["sub_Category_id"]
            else:
                getProduct["sub_category"] = advertisementList[0]["sub_Category_id"]
            getProduct["size"] = getProduct["size"] + advertisementList[0]["product_size_id"]

        Query = [{"is_active": 1}, {"is_delete": 1},
                 {"product_name": {"$regex": getProduct["search"], "$options": "i"}},
                 {"$expr": {
                     "$cond": {"if": {"$ne": [advertisementList[0]["product_from"], ""]}, "then":
                         {"$lte": [advertisementList[0]["product_from"], "$created_date"]},
                               "else": "true"}}},
                 {"$expr": {
                     "$cond": {"if": {"$ne": [advertisementList[0]["product_to"], ""]}, "then":
                         {"$gte": [advertisementList[0]["product_from"], "$created_date"]},
                               "else": "true"}}}
                 ]
        if len(getProduct["sleeve_pattern"]) > 0:
            Query.append({"sleeve_Pattern_id": {"$in": getProduct["sleeve_pattern"]}})
        if len(getProduct["product_type"]) > 0:
            Query.append({"product_type_id": {"$in": getProduct["product_type"]}})
        if len(getProduct["fabric_type"]) > 0:
            Query.append({"fabric_type_id": {"$in": getProduct["fabric_type"]}})
        if len(getProduct["category"]) > 0:
            Query.append({"category_id": {"$in": getProduct["category"]}})
        if len(getProduct["occasion"]) > 0:
            Query.append({"occasion_id": {"$in": getProduct["occasion"]}})
        if len(getProduct["neck_design"]) > 0:
            Query.append({"neck_design_id": {"$in": getProduct["neck_design"]}})

        Query2 = [{"$eq": ["$product_id", "$$product"]}, {"$eq": ["$is_delete", 1]},
                  {"$gte": ["$price", getProduct["price_start_range"]]},
                  {
                      "$cond": {"if": {"$gt": [getProduct["price_end_range"], 1]}, "then":
                          {"$lte": ["$price", getProduct["price_end_range"]]},
                                "else": "true"}}
                  ]
        if len(getProduct["size"]) > 0:
            Query2.append({"$in": ["$size_id", getProduct["size"]]})
        if len(getProduct["color"]) > 0:
            Query2.append({"$in": ["$color_family", getProduct["color"]]})

        productList = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": Query}},
                {"$lookup": {
                    "from": "sub_product",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": Query2}}},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],
                    "as": "sub_product"}},
                {"$lookup": {
                    "from": "wishlist",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [{"$eq": ["$user_id", getProduct["user_id"]]},
                                                       {"$eq": ["$product_id", "$$product"]}]
                                              }
                                    }}
                    ],
                    "as": "wishlist"
                }},
                {"$lookup": {
                    "from": "ratting",
                    "let": {"product": "$product_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}]}}}
                    ],
                    "as": "rattingData"
                }},
                {"$match": {
                    "$expr": {"$gt": [{"$size": "$sub_product"}, 0]}
                }},
                {"$addFields": {"rattingCount": {"$size": "$rattingData"},
                                "totalRatting": {"$sum": "$rattingData.ratting_value"},
                                "totalQuantity": {"$sum": "$sub_product.quantity"}}},
                {
                    "$project": {
                        "_id": {"$toString": "$_id"},
                        "category_id": 1,
                        "totalQuantity": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "product_name": 1,
                        "product_id": 1,
                        "is_active": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "dress_length": 1,
                        "dress_weight": 1,
                        "fitting": 1,
                        "sub_product.sub_product_id": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.size_id": 1,
                        "sub_product.color": 1,
                        "sub_product.images": 1,
                        "sub_product.price": 1,
                        "sub_product.quantity": 1,
                        "sub_product.cost_per_item": 1,
                        "sub_product.profit": 1,
                        "sub_product.margin": 1,
                        "sub_product.color_family": 1,
                        "wishlist.is_active": 1,
                        "rattingTotal": {
                            "$cond": {
                                "if": {"$ne": ["$totalRatting", 0]},
                                "then": {"$divide": ["$totalRatting", "$rattingCount"]},
                                "else": 0
                            }
                        },
                    }
                },
                {"$sort": {"product_id": -1}},  # Sorting by product_id in descending order
                {
                    "$facet": {
                        "data": [
                            {'$skip': getProduct["skip"]},
                            {"$limit": getProduct["limit"]}
                        ],
                        "pagination": [
                            {"$count": "total"}
                        ]
                    }
                }
            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = productList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_product(request: Request, product_details_model: get_product_details_model = Body(...)):
    response = {}
    try:
        productDetails = jsonable_encoder(product_details_model)
        productList = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": [{"product_id": productDetails["product_id"]}]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},

                    "pipeline": [

                        {"$match": {"$expr": {"$and": [{"$eq": ["$is_active", 1]}, {"$eq":["$is_delete", 1]},
                                                       {"$eq": ["$product_id", "$$product"]}]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},

                {"$lookup": {
                    "from": "wishlist",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [

                        {"$match": {"$expr": {"$and": [{"$eq": ["$user_id", productDetails["user_id"]]},
                                                       {"$eq": ["$product_id", "$$product"]}]
                                              }
                                    }}
                    ],
                    "as": "wishlist"
                }},
                {"$lookup": {
                    "from": "sleeve_pattern",
                    "localField": "sleeve_Pattern_id",
                    "foreignField": "sleeve_pattern_id",
                    "as": "sleeve_pattern"
                }},
                {"$lookup": {
                    "from": "occasion",
                    "localField": "occasion_id",
                    "foreignField": "occasion_id",
                    "as": "occasion"
                }},
                {"$lookup": {
                    "from": "product_type",
                    "localField": "product_type_id",
                    "foreignField": "product_type_id",
                    "as": "product_type"
                }},
                {"$lookup": {
                    "from": "fabric_type",
                    "localField": "fabric_type_id",
                    "foreignField": "fabric_id",
                    "as": "fabric_type"
                }},
                {"$lookup": {
                    "from": "neck_design",
                    "localField": "neck_design_id",
                    "foreignField": "neck_design_id",
                    "as": "neck_design"
                }},
                {"$lookup": {
                    "from": "ratting",
                    # "localField": "neck_design_id",
                    # "foreignField": "neck_design_id",
                    "let": {"product": "$product_id"},
                    "pipeline": [

                        {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}]}}}
                    ],
                    "as": "rattingData"
                }},
                {"$addFields": {"rattingCount": {"$size": "$rattingData"},
                                "totalRatting": {"$sum": "$rattingData.ratting_value"},
                                "totalQuantity": {"$sum": "$sub_product.quantity"}
                                }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "category_id": 1,
                        "totalQuantity": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "product_name": 1,
                        "product_id": 1,
                        "is_active": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "dress_length": 1,
                        "dress_weight": 1,
                        "size_chart_image":1,
                        "fitting": 1,
                        "no_size": 1,
                        'description': 1,
                        # 'expense': 1,
                        "product_url": 1,
                        "sub_product.sub_product_id": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.size_id": 1,
                        "sub_product.color": 1,
                        "sub_product.images": 1,
                        "sub_product.price": 1,
                        "sub_product.quantity": 1,
                        "sub_product.cost_per_item": 1,
                        "sub_product.profit": 1,
                        "sub_product.margin": 1,
                        "wishlist.is_active": 1,
                        "sleeve_pattern.sleeve_pattern_Name": 1,
                        "occasion.occasion_Name": 1,
                        "product_type.product_type_name": 1,
                        "fabric_type.fabric_name": 1,
                        "neck_design.neck_design_Name": 1,
                        "rattingTotal": {
                            "$cond":
                                {
                                    "if": {
                                        "$ne": [
                                            "$totalRatting",
                                            0
                                        ]
                                    }, "then":
                                    {"$divide": ["$totalRatting", "$rattingCount"]},
                                    "else": 0
                                }},

                    }
                }

            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = productList
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_similar_product_list(request: Request, id: str):
    response = {}
    try:
        productList = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": [{"product_id": id}]}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "category_id": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "product_name": 1,
                        "product_id": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                    }
                }
            ]))

        similarData = list(get_collection_product(request).aggregate(
            [
                {"$match": {"$and": [{"product_id": {"$ne": id}},
                                     {"$or": [
                                         {"$expr": {
                                             "$cond": {"if": {"$ne": [productList[0]["product_type_id"], "0"]}, "then":
                                                 {"$eq": [productList[0]["product_type_id"], "$product_type_id"]},
                                                       "else": "true"}}},
                                         {"product_name": {"$regex": productList[0]["product_name"], "$options": "i"}},
                                     ]}
                                     ]}},
                {"$lookup": {
                    "from": "sub_product",
                    # "localField": "product_id",
                    # "foreignField": "product_id",
                    "let": {"product": "$product_id"},

                    "pipeline": [

                        {"$match": {"$expr": {"$and": [{"is_active": 1}, {"is_delete": 1},
                                                       {"$eq": ["$product_id", "$$product"]}]
                                              }
                                    }},
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}],

                    "as": "sub_product"}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "category_id": 1,
                        "sub_Category_id": 1,
                        "product_type_id": 1,
                        "product_name": 1,
                        "product_id": 1,
                        "is_active": 1,
                        "occasion_id": 1,
                        "sleeve_Pattern_id": 1,
                        "fabric_type_id": 1,
                        "neck_design_id": 1,
                        "dress_length": 1,
                        "dress_weight": 1,
                        "fitting": 1,
                        "sub_product.sub_product_id": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.size_id": 1,
                        "sub_product.color": 1,
                        "sub_product.images": 1,
                        "sub_product.price": 1,
                        "sub_product.quantity": 1,
                        "sub_product.cost_per_item": 1,
                        "sub_product.profit": 1,
                        "sub_product.margin": 1,
                    }
                }

            ]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = similarData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_sub_product(request: Request, sup_product: UpdateSubProduct = Body(...)):
    response = {}
    try:
        supProduct = jsonable_encoder(sup_product)
        sub_product_data = list(get_collection_sub_product(request).aggregate([
            {"$match": {"$and": [{"sub_product_id": supProduct['sub_product_id']}]}}]))
        total_quantity = supProduct["total_quantity"]
        supProduct["total_quantity"] = sub_product_data[0]["total_quantity"] + total_quantity
        supProduct["quantity"] = sub_product_data[0]["quantity"] + total_quantity
        updateSubProduct = get_collection_sub_product(request).update_one(
            {"sub_product_id": supProduct['sub_product_id']},
            {"$set": {
                "price": supProduct["price"],
                "cost_per_item": supProduct["cost_per_item"],
                "profit": supProduct["profit"],
                "quantity": supProduct["quantity"],
                "margin": supProduct["margin"],
                "total_quantity": supProduct["total_quantity"]
            }})
        updateSubProduct1 = get_collection_sub_product(request).update_many(
            {"product_id": sub_product_data[0]['product_id'], "color": sub_product_data[0]['color']},
            {"$set": {
                "images": supProduct['images']
            }})
        response["error_code"] = "9999"
        response["message"] = "Update Sup Product Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def add_sub_product(request: Request, sup_product: SubProductList = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(sup_product)

        for item in insertData['sub_product']:
            subcount = list(get_collection_sub_product(request).aggregate([{"$count": "myCount"}]))
            if len(subcount) != 0:
                sub_product_id = "SUBPROD" + '{:03}'.format(subcount[0]["myCount"] + 1)
            else:
                sub_product_id = "SUBPROD" + '{:03}'.format(1)
            item["sub_product_id"] = sub_product_id
            insertSubProduct = get_collection_sub_product(request).insert_one(item)
            # getData = list(get_collection_sub_product(request).aggregate([
            #     {"$match": {"$and": [{"product_id": item['product_id']}, {"color": item['color']}]}}]))
            # if len(getData)>0:
        response["error_code"] = "9999"
        response["message"] = "Add Sup Product Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_product_only(request: Request, id: str, update_product: UpdateProduct = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in update_product.dict().items() if v is not None}  # loop in the dict

        value = updateData["product_name"].lower()
        listData = []
        # listData = list(get_collection_product(request).aggregate(
        #     [{
        #         "$match": {"$and": [{
        #             "$expr": {"$eq": [{
        #                 "$toLower": "$product_name"
        #             }, value]}},
        #             {"product_id": {"$ne": id}, }
        #         ]}
        #     }]
        # ))
        if len(listData) <= 0:
            update_result = get_collection_product(request).update_one({"product_id": id},
                                                                       {"$set": updateData})
            response["error_code"] = "9999"
            response["message"] = "Product Update Successfully"
        else:
            response["error_code"] = "9998"
            response["message"] = "Already the Product is Exist"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def delete_product(request: Request,id:str):
    response = {}
    try:
        update_result = get_collection_product(request).update_one({"product_id": id},
                                                                   {"$set": {'is_delete':0}})
        response["error_code"] = "9999"
        response["message"] = "Product Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def delete_sub_product(request: Request,id:str):
    response = {}
    try:
        update_result = get_collection_sub_product(request).update_one({"sub_product_id": id},
                                                                   {"$set": {'is_delete': 0}})
        response["error_code"] = "9999"
        response["message"] = "Product Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def update_product_is_ctive(request: Request,id:str,update_product):
    response = {}
    try:
        update_data = {k: v for k, v in update_product.dict().items() if v is not None}  # loop in the dict
        update_result = get_collection_product(request).update_one({"product_id": id},
                                                                   {"$set": update_data})
        response["error_code"] = "9999"
        response["message"] = "Product Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response