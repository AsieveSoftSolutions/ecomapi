from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.addresses import UpdateAddress, UserAddress
from bson import ObjectId
import uuid

def get_collection_addrs(request: Request):
  return request.app.database["addresses"]
def get_collection_users(request: Request):
  return request.app.database["users"]

def create_addrs(request: Request, user: UserAddress = Body(...)):
    response = {}
    try:
        addrs = jsonable_encoder(user)
        # getuser =list(get_collection_users(request).find_one({"email": addrs["email"]}))
        # # if len(getuser) >0:
        # customer_id = "ADDR001"
        # count = list(get_collection_addrs(request).aggregate([{"$count": "myCount"}]))
        # if len(count) != 0:
        #     customer_id = "ADDR" + '{:03}'.format(count[0]["myCount"] + 1)
        # else:
        #     customer_id = "ADDR" + '{:03}'.format(1)
        # addrs["address_id"] = customer_id
        addrs["address_id"] = "ADDR" + str(uuid.uuid4()).replace('-', '')
        new_addrs = get_collection_addrs(request).insert_one(addrs)
        response["error_code"] = "9999"
        response["message"] = "Address Add Successfully"
        #created_addrs = get_collection_addrs(request).find_one({"_id": new_addrs.inserted_id})
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response




def list_addrs(request: Request, userid):
    response = {}
    try:
        addrs = list(get_collection_addrs(request).aggregate([{
            "$match": {"$and":[{"user_id":userid},{"is_active":1}]}
        },{"$project":{
            "_id": {
                "$toString": "$_id"
            },
            "user_id":1,
            "address_id":1,
            "first_name":1,
            "last_name":1,
            "country":1,
            "state":1,
            "city":1,
            "street":1,
            "pincode":1,
            "phone_number":1,
            "email":1,
        }}]))

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = addrs
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def find_addrs(request: Request, user_id: str):
    user_addrs = list(get_collection_addrs(request).find({"user_id": user_id}))
    if len(user_addrs):
        return user_addrs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User has no address yet.")

def update_addrs(request: Request, id: str, addrs: UpdateAddress = Body(...)):
    response = {}
    try:
        addrs = {k: v for k, v in addrs.dict().items() if v is not None} #loop in the dict
        if len(addrs) >= 1:
            update_result = get_collection_addrs(request).update_one({"address_id": id}, {"$set": addrs})
        response["error_code"] = "9999"
        response["message"] = "Address Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

def delete_addrs(request: Request, id: str):
    response = {}
    try:
        deleted_addrs = get_collection_addrs(request).delete_one({"address_id": id})
        response["error_code"] = "9999"
        response["message"] = "Address Deleted Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response

