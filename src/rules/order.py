from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.order import Order, UpdateOrder
from src.models.custom_model import (response_return_model, get_order_price_request,
                                     get_user_model, UpdateOrderDetails, get_wishlist_request)
from src.models.refund import Refund, UpdateRefund
from bson import ObjectId
import uuid
from typing import List
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
import src.config.credential as Credantial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import base64


def get_collection_order(request: Request):
    return request.app.database["order"]


def get_collection_Refund(request: Request):
    return request.app.database["refund"]


def get_collection_order_details(request: Request):
    return request.app.database["order_details"]


def get_collection_sub_product(request: Request):
    return request.app.database["sub_product"]


def create_order(request: Request, order: Order = Body(...)):
    response = {}
    try:
        insertData = jsonable_encoder(order)
        orderData = jsonable_encoder(order)
        del orderData['order_details']
        orderData["order_id"] = "oid-" + datetime.now().strftime("%d%m%y%H%M%S%f")
        insert = get_collection_order(request).insert_one(orderData)

        for item in insertData["order_details"]:
            subProductList = list(get_collection_sub_product(request).aggregate([
                {"$match": {"$and": [{"sub_product_id": item["sub_product_id"]}]}}]))
            if subProductList[0]["quantity"] > 0:
                quantity = subProductList[0]["quantity"] - item["quantity"]
                updateSubProduct = get_collection_sub_product(request).update_one(
                    {"sub_product_id": item["sub_product_id"]},
                    {"$set": {"quantity": quantity}})
            item["order_id"] = orderData["order_id"]
            item["order_details_id"] = 'odid-' + datetime.now().strftime("%d%m%y%H%M%S%f")
            insert = get_collection_order_details(request).insert_one(item)
        order_email_send(request, orderData["order_id"])
        response["error_code"] = "9999"
        response["message"] = "Order Add Successfully"
        response["data"] = [{"order_id": orderData["order_id"]}]
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_order(request: Request, id: str, update_order: UpdateOrder = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in update_order.dict().items() if v is not None}  # loop in the dict
        retVal = updateData.get("status")
        if retVal is not None:
            value = updateData["status"].lower()
            if value == 'c':
                orderData = list(get_collection_order(request).aggregate([{"$match": {"order_id": id}}]))
                subProductList = list(get_collection_sub_product(request).aggregate([
                    {"$match": {"$and": [{"sub_product_id": orderData[0]["sub_product_id"]}]}}]))
                quantity = subProductList[0]["quantity"] + orderData[0]["quantity"]
                updateSubProduct = get_collection_sub_product(request).update_one(
                    {"sub_product_id": orderData[0]["sub_product_id"]},
                    {"$set": {"quantity": quantity}})

        update_result = get_collection_order(request).update_one({"order_id": id}, {"$set": updateData})
        response["error_code"] = "9999"
        response["message"] = "Order Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_order_details(request: Request, id: str, update_order: UpdateOrderDetails = Body(...)):
    response = {}
    try:
        updateData = {k: v for k, v in update_order.dict().items() if v is not None}  # loop in the dict
        retVal = updateData.get("status")
        if retVal is not None:
            value = updateData["status"].lower()
            if value == 'c':
                orderData = list(get_collection_order(request).aggregate([{"$match": {"order_details_id": id}}]))
                subProductList = list(get_collection_sub_product(request).aggregate([
                    {"$match": {"$and": [{"sub_product_id": orderData[0]["sub_product_id"]}]}}]))
                quantity = subProductList[0]["quantity"] + orderData[0]["quantity"]
                updateSubProduct = get_collection_sub_product(request).update_one(
                    {"sub_product_id": orderData[0]["sub_product_id"]},
                    {"$set": {"quantity": quantity}})

        update_result = get_collection_order_details(request).update_one({"order_details_id": id}, {"$set": updateData})
        if updateData["delivery_status"] == 'shipped':
            order_shipped_email_send(request, id)
        if updateData["delivery_status"] == 'received':
            order_delivery_email_send(request, id)
        response["error_code"] = "9999"
        response["message"] = "Order Update Successfully"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_order_list(request: Request, user: get_user_model = Body(...)):
    response = {}
    try:
        users = jsonable_encoder(user)
        category_list = list(get_collection_order(request).aggregate(
            [
                # {"$match": {'$and': [
                #     {"order_id": o_id},
                #
                # ]}},
                {"$lookup": {
                    "from": "order_details",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product",
                            "localField": "product_id",
                            "foreignField": "product_id",
                            "as": "product"
                        }},
                        {"$lookup": {
                            "from": "sub_product",
                            "localField": "sub_product_id",
                            "foreignField": "sub_product_id",
                            "pipeline": [
                                {"$lookup": {
                                    "from": "product_size",
                                    "localField": "size_id",
                                    "foreignField": "size_id",
                                    "as": "product_size"
                                }}
                            ],
                            "as": "sub_product"
                        }},
                        {"$lookup": {
                            "from": "postal_service",
                            "localField": "postal_service_id",
                            "foreignField": "postal_service_id",
                            "as": "postal_service"
                        }},
                    ],

                    "as": "order_details"
                }},
                {
                    "$sort": {"created_date": -1}
                },
                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},
                {"$addFields": {"sub_total": {"$sum": "$order_details.total_price"},

                                }},

                {"$addFields": {"date": {"$toDate": "$created_date"}}},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details.order_details_id": 1,
                        "order_details.price": 1,
                        "order_details.total_price": 1,
                        "order_details.gst_price": 1,
                        "order_details.delivery_amount": 1,
                        "order_details.quantity": 1,
                        "city": 1,
                        "country": 1,
                        "state": 1,
                        "pincode": 1,
                        "phone_number": 1,
                        "email": 1,
                        "street": 1,
                        "first_name": 1,
                        "last_name": 1,
                        "delivery_amount": 1,
                        "total_price": 1,
                        "sub_total": 1,
                        "order_id": 1,
                        "order_details.product.product_name": 1,
                        "order_details.sub_product.product_size.size_Name": 1,
                        "order_details.sub_product.images": 1,
                        "order_details.sub_product.color_family": 1,
                        "users.user_name": 1,
                        "users.email": 1,
                        "order_details.postal_service.postal_service_name": 1,
                        "order_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$date"}},
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
            ]

        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_user_order_list(request: Request, requestData: get_wishlist_request = Body(...)):
    response = {}
    try:
        request_data = jsonable_encoder(requestData)
        category_list = list(get_collection_order(request).aggregate(
            [
                {"$match": {"user_id": request_data["user_id"]}},
                {"$lookup": {
                    "from": "order_details",
                    # "localField": "order_id",
                    # "foreignField": "order_id",
                    "let": {"order_id": "$order_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$and": [
                            {"$eq": ["$order_id", "$$order_id"]},
                            {
                                "$cond": {"if": {"$ne": [request_data["status"], 'All']}, "then":
                                    {"$eq": ["$delivery_status", request_data["status"]]},
                                          "else": "true"}}
                        ]

                        }
                        }},
                        {"$lookup": {
                            "from": "product",
                            "localField": "product_id",
                            "foreignField": "product_id",
                            "as": "product"
                        }},
                        {"$lookup": {
                            "from": "sub_product",
                            "localField": "sub_product_id",
                            "foreignField": "sub_product_id",
                            "pipeline": [
                                {"$lookup": {
                                    "from": "product_size",
                                    "localField": "size_id",
                                    "foreignField": "size_id",
                                    "as": "product_size"
                                }}],
                            "as": "sub_product"
                        }},
                        {"$lookup": {
                            "from": "ratting",
                            "localField": "order_details_id",
                            "foreignField": "order_details_id",
                            "as": "ratting"
                        }},

                    ],
                    "as": "order_details"
                }
                },

                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"}},
                {"$match": {
                    "$expr": {"$gt": [
                        {"$size": "$order_details"},
                        0
                    ]}
                }},
                {
                    "$sort": {"created_date": -1}
                },
                # {
                #     "$addFields": {
                #         "c_Date": {
                #             "$toDate": "$created_date",
                #         }
                #     }
                # },

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
                        "order_id": 1,
                        "price": 1,
                        "total_price": 1,
                        "delivery_amount": 1,
                        "quantity": 1,
                        "first_name": 1,
                        "last_name": 1,
                        "country": 1,
                        "state": 1,
                        "city": 1,
                        "pincode": 1,
                        "phone_number": 1,
                        "email": 1,
                        "transaction_status": 1,
                        "order_details.price": 1,
                        "order_details.total_price": 1,
                        "order_details.gst_price": 1,
                        "order_details.quantity": 1,
                        "order_details.order_details_id": 1,
                        "order_details.delivery_status": 1,
                        "order_details.delivery_amount": 1,
                        "order_details.track_id": 1,
                        "order_details.product_id": 1,
                        "order_details.sub_product_id": 1,
                        "order_details.ratting.is_active": 1,
                        "order_details.ordered_date": 1,
                        "order_details.shipped_date": 1,
                        "order_details.delivery_date": 1,
                        "order_details.ratting_date": 1,
                        "order_details.expected_delivery_date": 1,
                        "order_details.product.product_name": 1,
                        "order_details.sub_product.images": 1,
                        "order_details.sub_product.product_size.size_Name": 1,
                    }
                }, {
                "$facet": {
                    "data": [
                        {'$skip': request_data["skip"]},
                        {"$limit": request_data["limit"]}
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


def get_order_details_list(request: Request, requestData: get_wishlist_request = Body(...)):
    response = {}
    try:
        request_data = jsonable_encoder(requestData)
        category_list = list(get_collection_order_details(request).aggregate(
            [
                {"$match": {'$and': [
                    {"order_details_id": {"$regex": request_data["search"], "$options": "i"}},
                    {"$expr": {
                        "$cond": {"if": {"$ne": [request_data["status"], 'All']}, "then":
                            {"$eq": ["$delivery_status", request_data["status"]]},
                                  "else": "true"}
                    }},
                    {"$expr": {
                        "$cond": {"if": {"$and": [{"$ne": [request_data["from_date"], '']},
                                                  {"$ne": [request_data["to_date"], '']}]}, "then":
                                      {"$gte": ["$ordered_date", request_data["from_date"]]},
                                  "else": "true"}
                    }},
                    {"$expr": {
                        "$cond": {"if": {"$and": [{"$ne": [request_data["from_date"], '']},
                                                  {"$ne": [request_data["to_date"], '']}]}, "then":
                                      {"$lte": ["$ordered_date", request_data["to_date"]]},
                                  "else": "true"}
                    }},
                ]}},
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {"$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product"
                }},
                {"$lookup": {
                    "from": "sub_product",
                    "localField": "sub_product_id",
                    "foreignField": "sub_product_id",
                    "as": "sub_product"
                }},
                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},
                {
                    "$sort": {"created_date": -1}
                },
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details_id": 1,
                        "order_id": 1,
                        "user_id": 1,
                        "product_id": 1,
                        "sub_product_id": 1,
                        "price": 1,
                        "total_price": 1,
                        "gst_price": 1,
                        "delivery_amount": 1,
                        "expected_delivery_date": 1,
                        "postal_service_id": 1,
                        "quantity": 1,
                        "delivery_status": 1,
                        "track_id": 1,
                        "ordered_date": 1,
                        "shipped_date": 1,
                        "delivery_date": 1,
                        "ratting_date": 1,
                        "order.city": 1,
                        "order.country": 1,
                        "order.state": 1,
                        "order.pincode": 1,
                        "order.phone_number": 1,
                        "order.email": 1,
                        "order.street": 1,
                        "product.product_name": 1,
                        "users.user_name": 1,
                    }
                }, {
                "$facet": {
                    "data": [
                        {'$skip': request_data["skip"]},
                        {"$limit": request_data["limit"]}
                    ],
                    "pagination": [
                        {"$count": "total"}
                    ]
                }
            }
            ]

        ))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_email_send(request: Request, o_id: str):
    response = {}
    try:
        category_list = list(get_collection_order(request).aggregate(
            [
                {"$match": {'$and': [
                    {"order_id": o_id},

                ]}},
                {"$lookup": {
                    "from": "order_details",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product",
                            "localField": "product_id",
                            "foreignField": "product_id",
                            "as": "product"
                        }},
                        {"$lookup": {
                            "from": "sub_product",
                            "localField": "sub_product_id",
                            "foreignField": "sub_product_id",
                            "pipeline": [
                                {"$lookup": {
                                    "from": "product_size",
                                    "localField": "size_id",
                                    "foreignField": "size_id",
                                    "as": "product_size"
                                }}
                            ],
                            "as": "sub_product"
                        }}],
                    "as": "order_details"
                }},

                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},
                {"$addFields": {"sub_total": {"$sum": "$order_details.total_price"},

                                }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details.order_details_id": 1,
                        "order_details.price": 1,
                        "order_details.total_price": 1,
                        "order_details.gst_price": 1,
                        "order_details.delivery_amount": 1,
                        "order_details.quantity": 1,
                        "city": 1,
                        "country": 1,
                        "state": 1,
                        "pincode": 1,
                        "phone_number": 1,
                        "email": 1,
                        "street": 1,
                        "first_name": 1,
                        "last_name": 1,
                        "delivery_amount": 1,
                        "total_price": 1,
                        "sub_total": 1,
                        "order_id": 1,
                        "order_details.product.product_name": 1,
                        "order_details.sub_product.product_size.size_Name": 1,
                        "order_details.sub_product.images": 1,
                        "users.user_name": 1,
                        "users.email": 1,
                    }
                }
            ]

        ))
        msg = MIMEMultipart()
        table_content = '';
        header = 'Thank You For Your Order'
        name = category_list[0]['first_name'] + ' ' + category_list[0]['last_name']
        #         table_content2 = f"""   <tr style=" border:1px solid #000000">
        #                     <td colspan="2" style="text-align: left;padding: 10px 3px;
        #                      border:1px solid #000000"
        #                     >Sub Total : </td>
        #                     <td  style="text-align: center;padding: 10px 3px;  border:1px solid #000000" >₹ {category_list[0]['sub_total']}</td>
        #                 </tr>
        # """
        #         if category_list[0]["delivery_amount"] > 0:
        #             table_content2 = table_content2 + f"""
        #  <tr style=" border:1px solid #000000">
        #                     <td colspan="2" style="text-align: left;padding: 10px 3px;  border:1px solid #000000" >Delivery Charge : </td>
        #                     <td  style="text-align: center;padding: 10px 3px;  border:1px solid #000000" >₹ {category_list[0]['delivery_amount']}</td>
        #                 </tr>"""
        #         if category_list[0]["total_price"] - category_list[0]['sub_total'] - category_list[0]['delivery_amount'] > 0:
        #             table_content2 = table_content2 + f"""
        #               <tr style=" border:1px solid #000000">
        #                     <td colspan="2" style="text-align: left ;padding: 10px 3px; border:1px solid #000000" >GST : </td>
        #                     <td  style="text-align: center ;padding: 10px 3px; border:1px solid #000000" >₹ {category_list[0]["total_price"] - category_list[0]['sub_total'] - category_list[0]['delivery_amount']}</td>
        #                 </tr>
        # """
        #         table_content2 = table_content2 + f"""
        #          <tr style=" border:1px solid #000000">
        #                     <td colspan="2"  style="text-align: left;padding: 10px 3px; border:1px solid #000000" >Total : </td>
        #                     <td  style="text-align: center;padding: 10px 3px; border:1px solid #000000" >₹ {category_list[0]["total_price"]}
        #                     </td>
        #                 </tr>
        # """
        #         for item in category_list[0]['order_details']:
        #             size = "Size:" + item["sub_product"][0]["product_size"][0]["size_Name"] if len(
        #                 item["sub_product"][0]["product_size"]) > 0 and item["sub_product"][0]["product_size"][0][
        #                                                                                            "size_Name"] else ''
        #             table_content = table_content + f"""
        #                 <tr style="border-collapse:collapse; border:1px solid #000000;text-align:left;">
        #                     <td style="border-collapse:collapse; padding: 10px 3px; border:1px solid #00000 ;text-align:left;">
        #                         <div>{item["order_details_id"]}</div>
        #                          <div>{item["product"][0]["product_name"]}</div>
        #                           <div> {size}</div>
        #                     </td>
        #                     <td style="border-collapse:collapse;padding: 10px 3px; border:1px solid #000000 ;text-align:center;">{item["quantity"]}</td>
        #                     <td style="border-collapse:collapse;padding: 10px 3px; border:1px solid #000000;text-align:center;">₹ {item["total_price"]}</td>
        #                 </tr>
        #         """
        #         address_content = f"""   <div style="border:1px solid #000000;padding: 5px;width: fit-content;margin-top:2px">
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{name}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["street"]}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["city"]}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["state"] + ' - ' + category_list[0]["pincode"]}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["country"]}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["phone_number"]}</div>
        #                     <div style="color: #0a1015;font-size: 15px;margin-top: 2px;">{category_list[0]["email"]}</div>
        #                 </div>"""
        deliveryStartDate = (
                datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") + timedelta(days=10)).strftime(
            "%b %d, %Y")
        deliveryEndDate = (
                datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") + timedelta(days=15)).strftime(
            "%b %d, %Y")
        currentDate = datetime.now().strftime("%b %d, %Y")
        order_details = ''
        for item in category_list[0]['order_details']:
            p_image = Credantial.imageView + item['sub_product'][0]['images'][0] if len(
                item['sub_product']) > 0 and len(
                item['sub_product'][0]['images']) > 0 else ''
            size = f"""<span style="font-size:15px">Size <span style="font-weight: 600;">{item["sub_product"][0]["product_size"][0]["size_Name"]} | </span></span>
                    """ if len(item["sub_product"]) > 0 and len(item["sub_product"][0]['product_size']) > 0 else ''
            sizeQty = f"""<div> {size}<span style="font-size:15px"> Qty
            <span style="font-weight: 600;"> {item["quantity"]}</span></span>"""
            order_details = order_details + f"""
             <tr>
                                    <td>
                                        <div>
                                            <img src={p_image}
                                                 style="height:100px;border-radius:3px">
                                        </div>
                                    </td>
                                    <td style="padding:10px; width:80% ">
                                        <div style="font-size:15px">
                                        {item["order_details_id"]}
                                        </div>
                                           <div style="font-size:15px">
                                         {item["product"][0]["product_name"]}
                                        </div>
                                      {sizeQty}
                                    </td>
                                    <td>₹ {item["total_price"]}
                                    </td>
                                </tr>"""
        citySatate = category_list[0]['city'] + ", " + category_list[0]['city'] + "," if \
            category_list[0]['city'] != '' else ''
        address = category_list[0]['street'] + ',' + citySatate + ' ' + category_list[0]['pincode']
        f = open(os.getcwd() + '/src/template/orderedtemplate.html', 'r')
        mail_content = f.read()
        # mail_content = (mail_content.replace("##tablecontent##", table_content).replace("##name##", name)
        #                 .replace('##current_date##', currentDate).replace('##tablecontent2##', table_content2).replace(
        #     '##address_content##', address_content)
        #                 .replace('##header##', header))
        mail_content = (mail_content.replace("##Name##", name).replace('##curant_date##', currentDate)
                        .replace('##tableContent##', order_details).
                        replace(' ##address##', address).replace("##start##", deliveryStartDate).
                        replace("##end##", deliveryEndDate).replace("##OrderId##", category_list[0]['order_id']))

        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'Order Successfully'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = category_list[0]["email"]
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], category_list[0]["email"],
                            msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_shipped_email_send(request: Request, o_id: str):
    response = {}
    try:
        category_list = list(get_collection_order_details(request).aggregate(
            [
                {"$match": {'$and': [
                    {"order_details_id": o_id},

                ]}},
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {"$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product"
                }},
                {"$lookup": {
                    "from": "sub_product",
                    "localField": "sub_product_id",
                    "foreignField": "sub_product_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}
                    ],
                    "as": "sub_product"
                }},
                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},
                {"$lookup": {
                    "from": "postal_service",
                    "localField": "postal_service_id",
                    "foreignField": "postal_service_id",
                    "as": "postal_service"
                }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details_id": 1,
                        "price": 1,
                        "total_price": 1,
                        "gst_price": 1,
                        "delivery_amount": 1,
                        "quantity": 1,
                        "track_id": 1,
                        "postal_service.url": 1,
                        "product.product_name": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.images": 1,
                        "users.user_name": 1,
                        "users.email": 1,
                        "order.email": 1,
                    }
                }
            ]

        ))
        msg = MIMEMultipart()
        p_image = Credantial.imageView + category_list[0]['sub_product'][0]['images'][0] if len(
            category_list[0]['sub_product']) > 0 and len(
            category_list[0]['sub_product'][0]['images']) > 0 else ''

        p_link = category_list[0]["postal_service"][0]["url"] if len(category_list[0]["postal_service"]) > 0 else ''

        size = "Size: " + category_list[0]["sub_product"][0]["product_size"][0]["size_Name"] if len(
            category_list[0]["sub_product"][0]["product_size"]) > 0 else ''
        table_content = f"""
      <tr>
       <td>
                    <div>
                        <img src={p_image}
                             style="height: 70px;" >
                    </div>
                </td>
                <td style="padding-left: 5px;">
                    <div style="margin-top: 5px;font-size: 15px;color: black;">Qty: &times;{category_list[0]['quantity']}</div>
                    <div style="margin-top: 5px;font-size: 15px;color: black;"> {size}</div>
                    <div style="margin-top: 5px;font-size: 15px;color: black;">Price: &#8377;{category_list[0]['total_price']}</div>
                </td>
            </tr>"""

        f = open(os.getcwd() + '/src/template/shippedtemplate.html', 'r')
        mail_content = f.read()
        mail_content = (mail_content.replace("##tablecontent##", table_content).replace("##track_id##",
                                                                                        category_list[0]["track_id"])
                        .replace("##link##", p_link))

        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'Order Shipped Successfully'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = category_list[0]["order"][0]["email"]
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], category_list[0]["order"][0]["email"],
                            msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_delivery_email_send(request: Request, o_id: str):
    response = {}
    try:
        category_list = list(get_collection_order_details(request).aggregate(
            [
                {"$match": {'$and': [
                    {"order_details_id": o_id},

                ]}},
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {"$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product"
                }},
                {"$lookup": {
                    "from": "sub_product",
                    "localField": "sub_product_id",
                    "foreignField": "sub_product_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}
                    ],
                    "as": "sub_product"
                }},
                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},

                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details_id": 1,
                        "price": 1,
                        "total_price": 1,
                        "gst_price": 1,
                        "delivery_amount": 1,
                        "quantity": 1,
                        "track_id": 1,
                        "product.product_name": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.images": 1,
                        "users.user_name": 1,
                        "users.email": 1,
                        "order.city": 1,
                        "order.country": 1,
                        "order.state": 1,
                        "order.pincode": 1,
                        "order.phone_number": 1,
                        "order.email": 1,
                        "order.street": 1,
                        "order.first_name": 1,
                        "order.last_name": 1,
                    }
                }
            ]

        ))
        msg = MIMEMultipart()
        currentDate = datetime.now().strftime("%b %d, %Y")
        p_image = Credantial.imageView + category_list[0]['sub_product'][0]['images'][0] if len(
            category_list[0]['sub_product']) > 0 and len(
            category_list[0]['sub_product'][0]['images']) > 0 else ''
        citySatate = category_list[0]["order"][0]['city'] + ", " + category_list[0]["order"][0]['city'] + "," if \
            category_list[0]["order"][0]['city'] != '' else ''
        address = category_list[0]["order"][0]['street'] + ',' + citySatate + ' ' + category_list[0]["order"][0][
            'pincode']
        name = category_list[0]["order"][0]['first_name'] + " " + category_list[0]["order"][0]['last_name']
        size = f"""
              <span style="font-size:15px">Size <span style="font-weight: 600;">{category_list[0]["sub_product"][0]["product_size"][0]["size_Name"]} | </span></span>
                                            
""" if len(category_list[0]["sub_product"]) > 0 and len(category_list[0]["sub_product"][0]['product_size']) > 0 else ''
        sizeQty = f"""<div>     {size}
                                             <span style="font-size:15px"> Qty<span
                                                    style="font-weight: 600;"> {category_list[0]["quantity"]}</span></span>

                                        </div>"""
        f = open(os.getcwd() + '/src/template/deliverytemplate.html', 'r')
        mail_content = f.read()
        mail_content = (mail_content.replace("##Name##", name).replace("##product_name##",
                                                                       category_list[0]['product'][0]["product_name"])
                        .replace('##orderId##', category_list[0]['order_details_id']).replace(' ##size_qty##', sizeQty).
                        replace(' ##address##', address).replace("#p_image", p_image))

        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'Order Delivery Successfully'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = category_list[0]["order"][0]["email"]
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], category_list[0]["order"][0]["email"],
                            msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def get_order_price(request: Request, requestData: get_order_price_request = Body(...)):
    response = {}
    try:
        request_data = jsonable_encoder(requestData)
        order_count_list = list(get_collection_order_details(request).aggregate([
            {
                "$match": {
                    "order_id": request_data['order_id']
                }
            },
            {
                "$count": "order_count"
            },

        ]))
        category_list = []
        if order_count_list[0]["order_count"] > 1:
            category_list = list(get_collection_order_details(request).aggregate([
                {
                    "$match": {
                        "order_details_id": request_data['order_details_id']
                    }
                },
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "total_price": {"$add": ["$total_price", "$gst_price", ], },
                        "order.transaction_id": 1,
                    }
                }
            ]))
        else:
            category_list = list(get_collection_order_details(request).aggregate([
                {
                    "$match": {
                        "order_details_id": request_data['order_details_id']
                    }
                },
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "total_price": {"$add": ["$total_price", "$gst_price", "$delivery_amount"], },
                        "order.transaction_id": 1,
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


def update_order_refund(request: Request, requestData: Refund = Body(...)):
    response = {}
    try:
        request_data = jsonable_encoder(requestData)
        update_result = get_collection_order_details(request).update_one({
            "order_details_id": request_data["order_details_id"]},
            {"$set": {"delivery_status": "refund", "updated_date": request_data["created_date"],
                      "update_by": request_data["create_by"]}})
        request_data["refund_id"] = "rid-" + datetime.now().strftime("%d%m%y%H%M%S%f")
        insert = get_collection_Refund(request).insert_one(request_data)
        order_refund_email_send(request, request_data["order_details_id"])
        response["error_code"] = "9999"
        response["message"] = "Refund Add Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def order_refund_email_send(request: Request, o_id: str):
    response = {}
    try:
        category_list = list(get_collection_order_details(request).aggregate(
            [
                {"$match": {'$and': [
                    {"order_details_id": o_id},

                ]}},
                {"$lookup": {
                    "from": "order",
                    "localField": "order_id",
                    "foreignField": "order_id",
                    "as": "order"
                }},
                {"$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product"
                }},
                {"$lookup": {
                    "from": "sub_product",
                    "localField": "sub_product_id",
                    "foreignField": "sub_product_id",
                    "pipeline": [
                        {"$lookup": {
                            "from": "product_size",
                            "localField": "size_id",
                            "foreignField": "size_id",
                            "as": "product_size"
                        }}
                    ],
                    "as": "sub_product"
                }},
                {"$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "users"
                }},

                {
                    "$project": {
                        "_id": {
                            "$toString": "$_id"
                        },
                        "order_details_id": 1,
                        "price": 1,
                        "total_price": 1,
                        "gst_price": 1,
                        "delivery_amount": 1,
                        "quantity": 1,
                        "track_id": 1,
                        "product.product_name": 1,
                        "sub_product.product_size.size_Name": 1,
                        "sub_product.images": 1,
                        "users.user_name": 1,
                        "users.email": 1,
                        "order.city": 1,
                        "order.country": 1,
                        "order.state": 1,
                        "order.pincode": 1,
                        "order.phone_number": 1,
                        "order.email": 1,
                        "order.street": 1,
                        "order.first_name": 1,
                        "order.last_name": 1,
                    }
                }
            ]

        ))
        msg = MIMEMultipart()
        currentDate = datetime.now().strftime("%b %d, %Y")
        p_image = Credantial.imageView + category_list[0]['sub_product'][0]['images'][0] if len(
            category_list[0]['sub_product']) > 0 and len(
            category_list[0]['sub_product'][0]['images']) > 0 else ''
        # citySatate = category_list[0]["order"][0]['city'] + ", " + category_list[0]["order"][0]['city'] + "," if \
        #     category_list[0]["order"][0]['city'] != '' else ''
        # address = category_list[0]["order"][0]['street'] + ',' + citySatate + ' ' + category_list[0]["order"][0][
        #     'pincode']
        name = category_list[0]["order"][0]['first_name'] + " " + category_list[0]["order"][0]['last_name']
        size = f"""
              <span style="font-size:15px">Size <span style="font-weight: 600;">{category_list[0]["sub_product"][0]["product_size"][0]["size_Name"]} | </span></span>

""" if len(category_list[0]["sub_product"]) > 0 and len(category_list[0]["sub_product"][0]['product_size']) > 0 else ''
        sizeQty = f"""<div>     {size}
                                             <span style="font-size:15px"> Qty<span
                                                    style="font-weight: 600;"> {category_list[0]["quantity"]}</span></span>

                                        </div>"""
        f = open(os.getcwd() + '/src/template/refundtemplate.html', 'r')
        mail_content = f.read()
        mail_content = (mail_content.replace("##Name##", name).
                        replace("##product_name##", category_list[0]['product'][0]["product_name"])
                        .replace('##order_id##', category_list[0]['order_details_id'])
                        .replace(' ##size_qty##', sizeQty).replace("#p_image", p_image))

        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'Order Cancel'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = category_list[0]["order"][0]["email"]
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], category_list[0]["order"][0]["email"],
                            msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = category_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response
