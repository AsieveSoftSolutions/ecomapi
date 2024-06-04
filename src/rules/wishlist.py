from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.wishlist import Wishlist, UpdateWishlist
from src.models.custom_model import response_return_model, get_user_model, get_wishlist_cookies_request, get_wishlist_request,delete_wishList_request
from bson import ObjectId
import uuid


def get_collection_wishlist(request: Request):
    return request.app.database["wishlist"]


def get_collection_product(request: Request):
    return request.app.database["product"]


def add_wishlist(request: Request, wish: Wishlist = Body(...)):
    response = {}
    try:

        insertData = jsonable_encoder(wish)
        cartData = list(get_collection_wishlist(request).aggregate(
            [{"$match": {"$and": [{"product_id": insertData["product_id"]},
                                  {"user_id": insertData["user_id"]}]}}]))
        if len(cartData) <= 0:
            insertData["wishlist_id"] = "WISH" + str(uuid.uuid4()).replace('-', '')
            new_addrs = get_collection_wishlist(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Wishlist Add Successfully"
        else:
            response["error_code"] = "9999"
            response["message"] = "Wishlist Add Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def delete_wishlist(request: Request, wish: delete_wishList_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(wish)
        deleted_user = get_collection_wishlist(request).delete_one(
            {"product_id": getData['product_id'],"user_id": getData['user_id']})

        response["error_code"] = "9999"
        response["message"] = "Wishlist Delete Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_wishlist_list(request: Request,  wish: get_wishlist_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(wish)
        resultData = list(get_collection_wishlist(request).aggregate(
            [{"$match": {"$and": [{"user_id": getData["user_id"]},
                                  {"is_active": 1}, {"is_delete": 1}]}},

             {"$lookup": {
                 "from": "product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}, ]}}},
                 ],
                 "as": "product"
             }},
             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}]}}},
                     # {"$lookup": {
                     #     "from": "product_size",
                     #     "localField": "size_id",
                     #     "foreignField": "size_id",
                     #     "as": "product_size"
                     # }}
                 ],
                 "as": "sub_product"}},

             {
                 "$project": {
                     "_id": 0,
                     "card_id": 1,
                     "user_id": 1,
                     "product_id": 1,
                     "product.product_name":1,
                     "sub_product.sub_product_id": 1,
                     # "sub_product.product_size.size_Name": 1,
                     "sub_product.size_id": 1,
                     "sub_product.color": 1,
                     "sub_product.images": 1,
                     "sub_product.price": 1,
                     "sub_product.quantity": 1,
                     "sub_product.cost_per_item": 1,
                 }
             },{
                 "$facet": {
                     "data": [
                         {'$skip': getData["skip"]},
                         {"$limit": getData["limit"]}
                     ],
                     "pagination": [
                         {"$count": "total"}
                     ]
                 }
             }
             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_wishlist_for_cookies(request: Request, wish_ids: get_wishlist_cookies_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(wish_ids)
        resultData = list(get_collection_product(request).aggregate(
            [{"$match": {"$and": [{"product_id": {"$in": getData['product_id']}},
                                  {"is_active": 1}, {"is_delete": 1}]}},
             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]}]}}},
                     # {"$lookup": {
                     #     "from": "product_size",
                     #     "localField": "size_id",
                     #     "foreignField": "size_id",
                     #     "as": "product_size"
                     # }}
                 ],
                 "as": "sub_product"}},

             {
                 "$project": {
                     "_id": 0,
                     "product_id": 1,
                     "product_name":1,
                     "sub_product.sub_product_id": 1,
                     # "sub_product.product_size.size_Name": 1,
                     "sub_product.size_id": 1,
                     "sub_product.color": 1,
                     "sub_product.images": 1,
                     "sub_product.price": 1,
                     "sub_product.quantity": 1,
                     "sub_product.cost_per_item": 1,
                 }
             },
             {
                 "$facet": {
                     "data": [
                         {'$skip': getData["skip"]},
                         {"$limit": getData["limit"]}
                     ],
                     "pagination": [
                         {"$count": "total"}
                     ]
                 }
             },
             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
