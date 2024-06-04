from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.bank_details import Bank_Details,Update_bank_details
from bson import ObjectId


def get_collection_Bank(request: Request):
  return request.app.database["bank_details"]

def create_bank(request: Request, bank: Bank_Details = Body(...)):
    response = {}
    try:
        bank = jsonable_encoder(bank)
        # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
        # if len(getuser) >0:
        customer_id = "BANK001"
        bank_dateils = list(get_collection_Bank(request).aggregate(
            [{"$match": { "card_number":bank["card_number"]}}]))
        if len(bank_dateils) <0:
            count = list(get_collection_Bank(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "BANK" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "BANK" + '{:03}'.format(1)
            bank["bank_id"] = customer_id
            new_addrs = get_collection_Bank(request).insert_one(bank)
            response["error_code"] = "9999"
            response["message"] = "Bank Details Add Successfully"
        else:
            get_collection_Bank(request).update_one({"_id": bank_dateils[0]["_id"]},
                                                    {"$set":{"card_holder_name":bank["card_holder_name"],
                                                             "card_number":bank["card_number"],
                                                             "month_year":bank["month_year"],
                                                             "cvv_number":bank["cvv_number"],
                                                             "is_active":1,
                                                             "updated_date":bank["updated_date"]
                                                     }})
            response["error_code"] = "9999"
            response["message"] = "Already  Exist And Updated Successfully"
        #created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def get_bank_list(request: Request,id):
    response = {}
    try:
        bank_details = list(get_collection_Bank(request).aggregate(
            [{"$match": {"$and": [{"user_id": id},
                                  {"is_active":1}]}},
             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "bank_id": 1,
                     "card_holder_name": 1,
                     "card_number": 1,
                     "month_year": 1,
                     "cvv_number": 1

                 }
             }
             ]))
        response["error_code"] = "9999"
        response["message"] = "Bank Details"
        response["data"] = bank_details
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def update_bank(request: Request, id: str, bank: Update_bank_details = Body(...)):
    response = {}
    try:
        banks = {k: v for k, v in bank.dict().items() if v is not None}  # loop in the dict
        update_result = get_collection_Bank(request).update_one({"bank_id": id}, {"$set": banks})
        response["error_code"] = "9999"
        response["message"] = "Bank Details Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response