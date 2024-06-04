from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.advertisement import Advertisement, UpdateAdvertisement
from src.models.custom_model import response_return_model, get_user_model, get_product_model
from bson import ObjectId
from datetime import datetime, date


def get_collection_advertisement(request: Request):
    return request.app.database["advertisement"]


def get_collection_product(request: Request):
    return request.app.database["product"]


def create_advertisement(request: Request, advertisement: Advertisement = Body(...)):
    response = {}
    try:
        inserData = jsonable_encoder(advertisement)
        Query = [{"is_active": 1}]
        if len(inserData["category_id"]) != 0:
            Query.append({"category_id": {"$in": inserData["category_id"]}})
        if len(inserData["sub_Category_id"]) != 0:
            Query.append({
                "$or": [{
                    'sub_Category_id': "0"
                }, {
                    "sub_Category_id": {"$in": inserData["sub_Category_id"]}
                }]})
        if len(inserData["product_type_id"]) != 0:
            Query.append({"product_type_id": {"$in": inserData["product_type_id"]}})
        if len(inserData["occasion_id"]) != 0:
            Query.append({"occasion_id": {"$in": inserData["occasion_id"]}})
        if len(inserData["fabric_type_id"]) != 0:
            Query.append({"fabric_type_id": {"$in": inserData["fabric_type_id"]}})
        if len(inserData["sleeve_Pattern_id"]) != 0:
            Query.append({"sleeve_Pattern_id": {"$in": inserData["sleeve_Pattern_id"]}})
        if len(inserData["neck_design_id"]) != 0:
            Query.append({"neck_design_id": {"$in": inserData["neck_design_id"]}})
        if inserData["product_from"] != "":
            date_string = inserData["product_from"]
            # date_object = datetime.strptime(date_string, '%a %b %d %Y')
            # new_date_string = date_object.strftime('%Y/%m/%d')
            Query.append({"created_date": {"$gte": inserData["product_from"]}})
        if inserData["product_to"] != "":
            date_string = inserData["product_to"]
            # date_object = datetime.strptime(date_string, '%a %b %d %Y')
            # new_date_string = date_object.strftime('%Y/%m/%d')
            Query.append({"created_date": {"$lte": inserData["product_to"]}})
        Query2 = [{"$eq": ["$product_id", "$$product"]}]
        if len(inserData["product_size_id"]) != 0:
            Query2.append({"$in": ["$size_id", inserData["product_size_id"]]})
        productList = list(get_collection_product(request).aggregate(
            [{"$match": {"$and": Query}},
             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [

                     {"$match": {"$expr": {"$and": Query2
                                           }
                                 }},
                 ],
                 "as": "sub_product"
             }},
             {"$addFields": {
                 "total_quantity": {"$sum": "$sub_product.quantity"}
             }
             },

             {
                 "$project": {
                     "_id": 0,
                     "total_quantity": 1,
                     # "category_id": 1,
                     # "totalQuantity": 1,
                     # "sub_Category_id": 1,
                     # "product_type_id": 1,
                     # "product_name": 1,
                     # "product_id": 1,
                     # "is_active": 1,
                     # "occasion_id": 1,
                     # "sleeve_Pattern_id": 1,
                     # "fabric_type_id": 1,
                     # "neck_design_id": 1,
                     # "sub_product.size_id": 1,
                 }
             }

             ]))
        sum_of_quantity = sum(item['total_quantity'] for item in productList)
        if len(productList) > 0:
            if sum_of_quantity > 0:
                value = inserData["coupon_code"].lower()
                advertisement_name = inserData["advertisement_name"].lower()
                listData = []
                if value != "":
                    listData = list(get_collection_advertisement(request).aggregate(
                        [{
                            "$match": {
                                "$expr": {"$eq": [{
                                    "$toLower": "$coupon_code"
                                }, value]}
                            }
                        }]
                    ))
                if len(listData) <= 0:

                    customer_id = "CAT001"
                    count = list(get_collection_advertisement(request).aggregate([{"$count": "myCount"}]))
                    if len(count) != 0:
                        customer_id = "AD" + '{:03}'.format(count[0]["myCount"] + 1)
                    else:
                        customer_id = "AD" + '{:03}'.format(1)
                    inserData["advertisement_id"] = customer_id
                    new_addrs = get_collection_advertisement(request).insert_one(inserData)
                    response["error_code"] = "9999"
                    response["message"] = "Advertisement Add Successfully"
                else:
                    response["error_code"] = "9998"
                    response["message"] = "Already the Coupon Code is Exist"
            else:
                response["error_code"] = "9998"
                response["message"] = "No Product Available this Filter"
        else:
            response["error_code"] = "9998"
            response["message"] = "No Product Available this Filter"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_advertisement(request: Request, id: str, update_advertisement: UpdateAdvertisement = Body(...)):
    response = {}
    try:
        inserData = jsonable_encoder(update_advertisement)
        update_data = {k: v for k, v in update_advertisement.dict().items() if v is not None}  # loop in the dict
        retVal = update_data.get("coupon_code")
        Query = [{"is_active": 1}]
        if retVal is not None:
            Query = [{"is_active": 1}]
            if len(inserData["category_id"]) != 0:
                Query.append({"category_id": {"$in": inserData["category_id"]}})
            if len(inserData["sub_Category_id"]) != 0:
                Query.append({
                    "$or": [{
                        'sub_Category_id': "0"
                    }, {
                        "sub_Category_id": {"$in": inserData["sub_Category_id"]}
                    }]})
            if len(inserData["product_type_id"]) != 0:
                Query.append({"product_type_id": {"$in": inserData["product_type_id"]}})
            if len(inserData["occasion_id"]) != 0:
                Query.append({"occasion_id": {"$in": inserData["occasion_id"]}})
            if len(inserData["fabric_type_id"]) != 0:
                Query.append({"fabric_type_id": {"$in": inserData["fabric_type_id"]}})
            if len(inserData["sleeve_Pattern_id"]) != 0:
                Query.append({"sleeve_Pattern_id": {"$in": inserData["sleeve_Pattern_id"]}})
            if len(inserData["neck_design_id"]) != 0:
                Query.append({"neck_design_id": {"$in": inserData["neck_design_id"]}})
            if inserData["product_from"] != "":
                date_string = inserData["product_from"]
                # date_object = datetime.strptime(date_string, '%a %b %d %Y')
                # new_date_string = date_object.strftime('%Y/%m/%d')
                Query.append({"created_date": {"$gte": inserData["product_from"]}})
            if inserData["product_to"] != "":
                date_string = inserData["product_to"]
                # date_object = datetime.strptime(date_string, '%a %b %d %Y')
                # new_date_string = date_object.strftime('%Y/%m/%d')
                Query.append({"created_date": {"$lte": inserData["product_to"]}})
            Query2 = [{"$eq": ["$product_id", "$$product"]}]
            if len(inserData["product_size_id"]) != 0:
                Query2.append({"$in": ["$size_id", inserData["product_size_id"]]})
            productList = list(get_collection_product(request).aggregate(
                [{"$match": {"$and": Query}},
                 {"$lookup": {
                     "from": "sub_product",
                     # "localField": "product_id",
                     # "foreignField": "product_id",
                     "let": {"product": "$product_id"},
                     "pipeline": [

                         {"$match": {"$expr": {"$and": Query2
                                               }
                                     }},
                     ],
                     "as": "sub_product"}},
                 {"$addFields": {
                     "total_quantity": {"$sum": "$sub_product.quantity"}
                 }
                 },

                 {
                     "$project": {
                         "_id": 0,
                         "total_quantity": 1,
                     }
                 }

                 ]))
            sum_of_quantity = sum(item['total_quantity'] for item in productList)
            if len(productList) > 0:
                if sum_of_quantity > 0:
                    value = update_data["coupon_code"].lower()
                    listData = []
                    if value != "":
                        listData = list(get_collection_advertisement(request).aggregate(
                            [{
                                "$match": {"$and": [{
                                    "$expr": {"$eq": [{
                                        "$toLower": "$coupon_code"
                                    }, value]}},
                                    {"advertisement_id": {"$ne": id}, }
                                ]}
                            }]
                        ))
                    if len(listData) <= 0:
                        update_result = get_collection_advertisement(request).update_one({"advertisement_id": id},
                                                                                         {"$set": update_data})
                        response["error_code"] = "9999"
                        response["message"] = "Advertisement Update Successfully"
                    else:
                        response["error_code"] = "9998"
                        response["message"] = "Already the Coupon Code is Exist"

                else:
                    response["error_code"] = "9998"
                    response["message"] = "No Product Available this Filter"
            else:
                response["error_code"] = "9998"
                response["message"] = "No Product Available this Filter"
        else:
            update_result = get_collection_advertisement(request).update_one({"advertisement_id": id},
                                                                             {"$set": update_data})
            response["error_code"] = "9999"
            response["message"] = "Advertisement Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_advertisement_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)
        fabric_type_list = list(get_collection_advertisement(request).aggregate(
            [{"$match": {"$and": [
                {"coupon_code": {"$regex": users["search"], "$options": "i"}}, {"is_delete": 1}
            ]}},
                # {
                #     "$skip": users["skip_count"]
                # },
                # {
                #     "$limit": users["limit"]
                # },
                {
                    "$sort": {"created_date": -1}
                },
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "advertisement_id": 1,
                        "coupon_code": 1,
                        "offer_percentage": 1,
                        "advertisement_name": 1,
                        "image": 1,
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
                }

            ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = fabric_type_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_active_advertisement_list(request):
    response = {}
    try:
        fabric_type_list = list(get_collection_advertisement(request).aggregate(
            [{"$match": {"$and": [
                {"is_active": 1}, {"is_delete": 1},
                {"$expr": {
                    "$cond": {"if": {"$ne": ["$validate_from", ""]}, "then":
                        {"$lte": ["$validate_from", datetime.today().strftime('%Y-%m-%d')]},
                              "else": "true"}}},
                {"$expr": {
                    "$cond": {"if": {"$ne": ["$validate_to", ""]}, "then":
                        {"$gte": ["$validate_to", datetime.today().strftime('%Y-%m-%d')]},
                              "else": "true"}}}
            ]}},
                # {"$lookup": {
                #     "from": "product",
                #     "let": {"active": "$is_active", "delete": "$is_delete", "category": "$category_id",
                #             "sub_Category": "$sub_Category_id", "product_type": "$product_type_id",
                #             "occasion": "$occasion_id", "sleeve_Pattern": "$sleeve_Pattern_id",
                #             "fabric_type": "$fabric_type_id", "neck_design": "$neck_design_id"},
                #
                #     "pipeline": [
                #
                #         {"$match": {"$expr": {"$and": [
                #             {"$eq": ["$is_active", 1]},
                #             {"$eq": ["$is_delete", 1]},
                #
                #             {"$cond": {"if": {"$ne": ["$$category", "0"]}, "then":
                #                 {"$eq": ["$category_id", "$$category"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$sub_Category", "0"]}, "then":
                #                 {"$eq": ["$sub_Category_id", "$$sub_Category"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$product_type", "0"]}, "then":
                #                 {"$eq": ["$product_type_id", "$$product_type"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$occasion", "0"]}, "then":
                #                 {"$eq": ["$occasion_id", "$$occasion"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$sleeve_Pattern", "0"]}, "then":
                #                 {"$eq": ["$sleeve_Pattern_id", "$$sleeve_Pattern"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$fabric_type", "0"]}, "then":
                #                 {"$eq": ["$fabric_type_id", "$$fabric_type"]},
                #                        "else": "true"}},
                #             {"$cond": {"if": {"$ne": ["$$neck_design", "0"]}, "then":
                #                 {"$eq": ["$neck_design_id", "$$neck_design"]},
                #                        "else": "true"}},
                #         ]}
                #         }},
                #         {"$lookup": {
                #             "from": "sub_product",
                #             "localField": "product_id",
                #             "foreignField": "product_id",
                #             "as": "sub_product"}},
                #     ],
                #     "as": "product"}},
                # {"$addFields": {
                #     "total_quantity": {"$sum": "$sub_product.quantity"}
                # }
                # },
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "advertisement_id": 1,
                        "coupon_code": 1,
                        "offer_percentage": 1,
                        "advertisement_name": 1,
                        "image": 1,
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
                        "is_active": 1,
                        # "product.product_name": 1,
                        # "product.sub_product.quantity":1,

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
