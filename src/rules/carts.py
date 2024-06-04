from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.carts import Carts, UpdateCarts
from src.models.custom_model import response_return_model, get_user_model, get_wishlist_request, \
    cart_quantity_update_request, cart_check_request, get_cookies_cart_list_request
from bson import ObjectId
import uuid
from typing import List


def get_collection_cart(request: Request):
    return request.app.database["carts"]


def get_collection_product(request: Request):
    return request.app.database["product"]


def add_cart(request: Request, cart: Carts = Body(...)):
    response = {}
    try:

        insertData = jsonable_encoder(cart)
        cartData = list(get_collection_cart(request).aggregate(
            [{"$match": {"$and": [{"product_id": insertData["product_id"]}, {"user_id": insertData["user_id"]},
                                  {"color": insertData["color"]}, {"size_id": insertData["size_id"]}]}}]))
        if len(cartData) <= 0:
            insertData["card_id"] = "CART" + str(uuid.uuid4()).replace('-', '')
            new_addrs = get_collection_cart(request).insert_one(insertData)
            response["error_code"] = "9999"
            response["message"] = "Cart Add Successfully"
        else:
            quantity1 = cartData[0]["quantity"] + insertData["quantity"]
            update_result = get_collection_cart(request).update_one({"card_id": cartData[0]["card_id"]}, {"$set": {
                "quantity": quantity1
            }})
            response["error_code"] = "9999"
            response["message"] = "Cart Add Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_cart(request: Request, id: str, cart: UpdateCarts = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in cart.dict().items() if v is not None}
        # updateData = jsonable_encoder(cart)
        update_result = get_collection_cart(request).update_one({"card_id": id}, {"$set": updateData})
        response["error_code"] = "9999"
        response["message"] = "Cart Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def delete_cart(request: Request, id: str):
    response = {}
    try:
        deleted_user = get_collection_cart(request).delete_one({"card_id": id})

        response["error_code"] = "9999"
        response["message"] = "Cart Delete Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def delete_multiple_cart(request: Request, cart: cart_check_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(cart)
        deleted_user = get_collection_cart(request).delete_many({"card_id": {'$in': getData['card_id']}})

        response["error_code"] = "9999"
        response["message"] = "Cart Delete Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_cart_list(request: Request, cart: get_wishlist_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(cart)
        resultData = list(get_collection_cart(request).aggregate(
            [{"$match": {"$and": [{"user_id": getData["user_id"]}]}},
             {"$lookup": {
                 "from": "product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                    {"$eq": ["$is_active", 1]},
                                                    {"$eq": ["$is_delete", 1]}
                                                    ]}}},
                 ],
                 "as": "product"
             }},
             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id", "color_code": "$color"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                    {"$eq": ["$color", "$$color_code"]}
                                                    ],
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
                     {"$match": {"$expr": {"$and": [{"$eq": ["$user_id", getData["user_id"]]},
                                                    {"$eq": ["$product_id", "$$product"]}]
                                           }
                                 }}
                 ],
                 "as": "wishlist"
             }},
             {"$match": {
                 "$expr": {"$and": [ {"$gt": [
                     {"$size": "$sub_product"},
                     0
                 ]},{"$gt": [
                     {"$size": "$product"},
                     0
                 ]}]}
             }},

             {
                 "$sort": {"updated_date": -1}
             },
             {
                 "$project": {
                     "_id": 0,
                     "card_id": 1,
                     "user_id": 1,
                     "product_id": 1,
                     "color": 1,
                     "size_id": 1,
                     "quantity": 1,
                     'product.no_size': 1,
                     "product.product_name": 1,
                     "sub_product.sub_product_id": 1,
                     "sub_product.product_size.size_Name": 1,
                     "sub_product.size_id": 1,
                     "sub_product.color": 1,
                     "sub_product.images": 1,
                     "sub_product.price": 1,
                     "sub_product.quantity": 1,
                     "sub_product.cost_per_item": 1,
                     "wishlist.is_active": 1,
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
                 }}
             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def cart_quantity_check(request: Request, cart: cart_check_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(cart)
        resultData = list(get_collection_cart(request).aggregate(
            [{"$match": {"$and": [{"card_id": {"$in": getData['card_id']}}]}},

             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id", "color_code": "$color", "size": "$size_id", "quantity": "$quantity"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                    {"$eq": ["$color", "$$color_code"]},
                                                    {"$eq": ["$size_id", "$$size"]},
                                                    {"$lt": ["$quantity", "$$quantity"]},
                                                    ]
                                           }
                                 }},
                 ],
                 "as": "sub_product"}},
             {
                 "$addFields": {
                     "countDishes": {
                         "$size": "$sub_product"
                     }
                 }
             },
             {
                 "$match": {
                     "countDishes": {
                         "$gt": 0
                     }
                 }},

             {
                 "$project": {
                     "_id": 0,
                     "card_id": 1,
                     "quantity": 1,
                     "sub_product.quantity": 1,
                     "sub_product.images": 1,
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


def update_cart_quantity(request: Request, cart: cart_quantity_update_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(cart)
        resultData = list(get_collection_cart(request).aggregate([
            {"$match": {"$and": [{"card_id": getData["cart_id"]}]}}]))
        if (getData["type"] == 'add'):
            quantity = resultData[0]["quantity"] + 1
            update_result = get_collection_cart(request).update_one(
                {"card_id": getData["cart_id"]}, {"$set": {"quantity": quantity}})
        else:
            quantity = resultData[0]["quantity"] - 1
            update_result = get_collection_cart(request).update_one(
                {"card_id": getData["cart_id"]}, {"$set": {"quantity": quantity}})
        response["error_code"] = "9999"
        response["message"] = "Cart Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_checkout_list(request: Request, cart: cart_check_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(cart)
        resultData = list(get_collection_cart(request).aggregate(
            [{"$match": {"$and": [{"card_id": {"$in": getData['card_id']}}]}},

             {"$lookup": {
                 "from": "product",
                 "localField": "product_id",
                 "foreignField": "product_id",
                 "let": {"quantity": "$quantity"},
                 "pipeline": [
                     {"$addFields": {
                         "product_weight": {"$multiply": ["$$quantity", "$dress_weight"]}}},
                 ],
                 "as": "product"}},

             {"$lookup": {
                 "from": "sub_product",
                 # "localField": "product_id",
                 # "foreignField": "product_id",
                 "let": {"product": "$product_id", "color_code": "$color", "size": "$size_id", "quantity": "$quantity"},
                 "pipeline": [
                     {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                    {"$eq": ["$color", "$$color_code"]},
                                                    {"$eq": ["$size_id", "$$size"]}, ]
                                           }
                                 }},
                     {"$addFields": {
                         "product_price": {"$multiply": ["$$quantity", "$price"]}}},
                 ],
                 "as": "sub_product"}},

             {
                 "$project": {
                     "_id": 0,
                     "card_id": 1,
                     "user_id": 1,
                     "product_id": 1,
                     "color": 1,
                     "size_id": 1,
                     "quantity": 1,
                     "product.product_weight": 1,
                     "sub_product.sub_product_id": 1,
                     "sub_product.size_id": 1,
                     "sub_product.color": 1,
                     "sub_product.images": 1,
                     "sub_product.price": 1,
                     "sub_product.quantity": 1,
                     "sub_product.cost_per_item": 1,
                     'sub_product.product_price': 1,
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


def get_cart_count(request: Request, id: str):
    response = {}
    try:
        resultData = list(get_collection_cart(request).aggregate([
            {
                "$match": {
                    "user_id": id
                }
            },
            {
                "$count": "total_count"
            }
        ]
        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_cookies_cart_list(request: Request, cart: List[get_cookies_cart_list_request] = Body(...)):
    response = {}
    try:
        requestData = jsonable_encoder(cart)
        resultData1 = []
        for item in requestData:
            resultData = list(get_collection_product(request).aggregate(
                [{"$match": {"$and": [{"product_id": item['product_id']},
                                      {"is_active": 1},
                                      {"is_delete": 1}
                                      ]}},

                 {"$lookup": {
                     "from": "sub_product",
                     # "localField": "product_id",
                     # "foreignField": "product_id",
                     "let": {"product": "$product_id"},
                     "pipeline": [
                         {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                        {"$eq": ["$color", item['color']]},
                                                        {"$eq": ["$is_delete", 1]}
                                                        ]
                                               }
                                     }},
                         {"$lookup": {
                             "from": "product_size",
                             "localField": "size_id",
                             "foreignField": "size_id",
                             "as": "product_size"
                         }}
                     ],
                     "as": "sub_product"}},
                 {"$match": {
                     "$expr": {"$gt": [
                         {"$size": "$sub_product"},
                         0
                     ]}
                 }},

                 {
                     "$project": {
                         "_id": 0,
                         'no_size': 1,
                         "product_id": 1,
                         "product_name": 1,
                         "sub_product.sub_product_id": 1,
                         "sub_product.size_id": 1,
                         "sub_product.color": 1,
                         "sub_product.images": 1,
                         "sub_product.price": 1,
                         "sub_product.quantity": 1,
                         "sub_product.cost_per_item": 1,
                         "sub_product.is_delete": 1,
                         'sub_product.product_price': 1,
                         "sub_product.product_size.size_Name": 1,
                     }
                 }
                 ]))
            resultData[0]['selected_size'] = item['size_id']
            resultData[0]['quantity'] = item['quantity']
            resultData[0]['selected_color'] = item['color']
            resultData1.append(resultData[0])
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData1
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def cookie_cart_quantity_check(request: Request, cart: List[get_cookies_cart_list_request] = Body(...)):
    response = {}
    try:
        requestData = jsonable_encoder(cart)
        resultData1 = []
        for item in requestData:
            resultData = list(get_collection_product(request).aggregate(
                [{"$match": {"$and": [{"product_id": item['product_id']}, {"is_active": 1},
                                      {"is_delete": 1}]}},

                 {"$lookup": {
                     "from": "sub_product",
                     # "localField": "product_id",
                     # "foreignField": "product_id",
                     "let": {"product": "$product_id"},
                     "pipeline": [
                         {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                        {"$eq": ["$color", item['color']]},
                                                        {"$eq": ["$size_id", item['size_id']]},
                                                        {"$lt": ["$quantity", item['quantity']]}]
                                               }
                                     }},
                     ],
                     "as": "sub_product"}},
                 {
                     "$addFields": {
                         "countDishes": {
                             "$size": "$sub_product"
                         }
                     }
                 },
                 {
                     "$match": {
                         "countDishes": {
                             "$gt": 0
                         }
                     }},

                 {
                     "$project": {
                         "_id": 0,
                         "product_id": 1,
                         "product_name": 1,
                         "sub_product.quantity": 1,
                         "sub_product.images": 1,
                     }
                 }
                 ]))
            if len(resultData) > 0:
                resultData1.append(resultData[0])
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData1
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_cookie_checkout_list(request: Request, cart: List[get_cookies_cart_list_request] = Body(...)):
    response = {}
    try:
        requestData = jsonable_encoder(cart)
        resultData1 = []
        for item in requestData:
            resultData = list(get_collection_product(request).aggregate(
                [{"$match": {"$and": [{"product_id": item['product_id']}, {"is_active": 1},
                                      {"is_delete": 1}]}},
                 {"$addFields": {
                     "product_weight": {"$multiply": [item['quantity'], "$dress_weight"]}}},
                 {"$lookup": {
                     "from": "sub_product",
                     # "localField": "product_id",
                     # "foreignField": "product_id",
                     "let": {"product": "$product_id"},
                     "pipeline": [
                         {"$match": {"$expr": {"$and": [{"$eq": ["$product_id", "$$product"]},
                                                        {"$eq": ["$color", item['color']]},
                                                        {"$eq": ["$size_id", item['size_id']]}]
                                               }
                                     }},
                         {"$addFields": {
                             "product_price": {"$multiply": [item['quantity'], "$price"]}}},
                     ],

                     "as": "sub_product"}},
                 {
                     "$addFields": {
                         "countDishes": {
                             "$size": "$sub_product"
                         }
                     }
                 },
                 {
                     "$match": {
                         "countDishes": {
                             "$gt": 0
                         }
                     }},

                 {
                     "$project": {
                         "_id": 0,
                         "product_id": 1,
                         # "color": 1,
                         # "size_id": 1,
                         # "quantity": 1,
                         "product_weight": 1,
                         "sub_product.sub_product_id": 1,
                         "sub_product.size_id": 1,
                         "sub_product.color": 1,
                         "sub_product.images": 1,
                         "sub_product.price": 1,
                         "sub_product.quantity": 1,
                         "sub_product.cost_per_item": 1,
                         'sub_product.product_price': 1,
                     }
                 }
                 ]))
            if len(resultData) > 0:
                resultData[0]['size_id'] = item['size_id']
                resultData[0]['quantity'] = item['quantity']
                resultData[0]['color'] = item['color']
                resultData1.append(resultData[0])
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = resultData1
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
