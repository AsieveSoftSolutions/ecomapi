from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.users import User, UpdateUser
from bson import ObjectId
from src.models.custom_model import login_model as LoginModel, change_password_request, get_new_arrivals_request, \
    forget_pwd_request
import os
import base64
import src.config.credential as Credantial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.models.otp import Otp, UpdateOtp
import math, random
import uuid
from datetime import datetime, timedelta


def get_collection_users(request: Request):
    return request.app.database["users"]


def get_collection_otp(request: Request):
    return request.app.database["otp"]


def create_user(request: Request, user: User = Body(...)):
    response = {}
    try:
        user = jsonable_encoder(user)
        customer_id = "0"

        getuser = list(get_collection_users(request).aggregate([{"$match": {"email": user["email"]}},
                                                                {
                                                                    "$project": {
                                                                        "_id": {
                                                                            "$toString": "$_id"
                                                                        },
                                                                        "user_id": 1,
                                                                        "user_name": 1,
                                                                        "email": 1,
                                                                        "role": 1

                                                                    }
                                                                }]
                                                               ))
        if len(getuser) == 0:
            count = list(get_collection_users(request).aggregate([{"$count": "myCount"}]))
            if len(count) != 0:
                customer_id = "CUS" + '{:03}'.format(count[0]["myCount"] + 1)
            else:
                customer_id = "CUS" + '{:03}'.format(1)
            user["user_id"] = customer_id

            new_user = get_collection_users(request).insert_one(user)
            createuser = list(get_collection_users(request).aggregate(
                [{"$match": {"_id": new_user.inserted_id}},
                 {
                     "$project": {
                         "_id": {
                             "$toString": "$_id"
                         },
                         "user_id": 1,
                         "user_name": 1,
                         "email": 1,
                         "role": 1

                     }
                 }
                 ]))
            send_verify_mail(user["email"], user["user_id"], user["user_name"])
            response["error_code"] = "9999"
            response["message"] = "Insert Successfully"
            response["data"] = createuser
        else:
            response["error_code"] = "9998"
            response["message"] = "Email Already Exist"
            response["data"] = getuser

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


def send_verify_mail(email_to: str, user_id: str, user_name: str):
    response = {}
    try:
        msg = MIMEMultipart()
        f = open(os.getcwd() + '/src/template/verifyemail.html', 'r')
        mail_content = f.read()
        dataBytes = user_id.encode("utf-8")
        login_link = Credantial.login_url + str(base64.b64encode(dataBytes).decode("utf-8"))
        print(str(base64.b64encode(dataBytes).decode("utf-8")), login_link)
        mail_content = (mail_content.replace("##name##", user_name)
                        .replace("##link##", login_link))
        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'mail'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = Credantial.email_credential['password']
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], email_to, msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Email sent successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = f"Failed to send email. Error: {str(e)}"

    return response


def user_login(request: Request, Login: LoginModel = Body(...)):
    response = {}
    try:
        Login = jsonable_encoder(Login)
        email_data = list(get_collection_users(request).aggregate(
            [{"$match": {"email": Login["email"]}}]))
        if Login['role'] == 1:
            if len(email_data) > 0:
                if email_data[0]['password'] == Login["password"]:
                    if email_data[0].get('verify_status') is not None and  email_data[0]['verify_status'] == 1  :
                        password_data = list(get_collection_users(request).aggregate(
                            [{"$match": {"$and": [{"email": Login["email"]},
                                                  {"password": Login["password"]}]}},
                             {
                                 "$project": {
                                     "_id": {
                                         "$toString": "$_id"
                                     },
                                     "user_id": 1,
                                     "user_name": 1,
                                     "email": 1,
                                     "role": 1
                                 }
                             }
                             ]))
                        response["error_code"] = "9999"
                        response["message"] = "Login Successfully"
                        response["data"] = password_data
                    else:
                        send_verify_mail(email_data[0]["email"], email_data[0]["user_id"], email_data[0]["user_name"])
                        response["error_code"] = "9997"
                        response["message"] = "Please Verify Your Email"
                else:
                    response["error_code"] = "9998"
                    response["message"] = "Password Incorrect"

            else:
                response["error_code"] = "9998"
                response["message"] = "Email Incorrect"
        else:
            if len(email_data) > 0:
                if email_data[0]['password'] == Login["password"]:

                    password_data = list(get_collection_users(request).aggregate(
                        [{"$match": {"$and": [{"email": Login["email"]},
                                              {"password": Login["password"]}]}},
                         {
                             "$project": {
                                 "_id": {
                                     "$toString": "$_id"
                                 },
                                 "user_id": 1,
                                 "user_name": 1,
                                 "email": 1,
                                 "role": 1

                             }
                         }
                         ]))
                    response["error_code"] = "9999"
                    response["message"] = "Login Successfully"
                    response["data"] = password_data

                else:
                    response["error_code"] = "9998"
                    response["message"] = "Password Incorrect"

            else:
                response["error_code"] = "9998"
                response["message"] = "Email Incorrect"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


def get_user_list(request: Request, user: User):
    response = {}
    try:
        Users = jsonable_encoder(user)
        user_list = list(get_collection_users(request).aggregate(
            [{"$match": {"$and": [{"is_active": 1}, {"role": 1},

                                  {"$or": [{"user_name": {"$regex": Users["search"], "$options": "i"}},
                                           {"email": {"$regex": Users["search"], "$options": "i"}}
                                           ]}]}
              },
             {"$lookup": {
                 "from": "addresses",
                 "localField": "user_id",
                 "foreignField": "user_id",
                 "as": "address"}},
             # {
             #     "$skip": Users["skip_count"]
             # },
             # {
             #     "$limit": Users["limit"]
             # },
             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "user_id": 1,
                     "user_name": 1,
                     "email": 1,
                     "role": 1,
                     "address.address_id": 1,
                     "address.first_name": 1,
                     "address.last_name": 1,
                     "address.country": 1,
                     "address.state": 1,
                     "address.city": 1,
                     "address.street": 1,
                     "address.pincode": 1,
                     "address.phone_number": 1,
                     "address.email": 1,
                     # "address_details":{ "$concat": ['address[0].street', ', ', 'address[0].city' ] }

                 }
             },
             {
                 "$facet": {
                     "data": [
                         {'$skip': Users["skip_count"]},
                         {"$limit": Users["limit"]}
                     ],
                     "pagination": [
                         {"$count": "total"}
                     ]
                 }
             },
             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = user_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)

    return response


def list_users(request: Request, limit: int):
    users = list(get_collection_users(request).find(limit=limit))
    return users


def find_user(request: Request, id: str):
    if (user := get_collection_users(request).find_one({"_id": ObjectId(id)})):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")


def delete_user(request: Request, id: str):
    deleted_user = get_collection_users(request).delete_one({"_id": ObjectId(id)})

    if deleted_user.deleted_count == 1:
        return f"User with id {id} deleted successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")


def get_user(request: Request, id: str):
    response = {}
    try:
        user_list = list(get_collection_users(request).aggregate(
            [{"$match": {"user_id": id}},

             {
                 "$project": {
                     "_id": {
                         "$toString": "$_id"
                     },
                     "user_id": 1,
                     "user_name": 1,
                     "email": 1,
                     "gender": 1,
                     "profile": 1,
                     "date_of_birth": 1,
                     "last_name": 1,
                 }
             }
             ]))
        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = user_list
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def update_user(request: Request, id: str, update_data: UpdateUser = Body(...)):
    response = {}
    try:
        update_data = {k: v for k, v in update_data.dict().items() if v is not None}  # loop in the dict
        update_result = get_collection_users(request).update_one({"user_id": id},
                                                                 {"$set": update_data})
        response["error_code"] = "9999"
        response["message"] = "User Update Successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def password_change(request: Request, change_pwd: change_password_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(change_pwd)
        user_list = list(get_collection_users(request).aggregate(
            [{"$match": {"user_id": getData['user_id']}}]))
        if user_list[0]['password'] == getData['old_pwd']:
            update_result = get_collection_users(request).update_one({"user_id": getData['user_id']},
                                                                     {"$set": {
                                                                         "password": getData['new_pwd']
                                                                     }})
            response["error_code"] = "9999"
            response["message"] = "Password Update Successfully"

        else:
            response["error_code"] = "9998"
            response["message"] = "Old Password Is Wrong"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def verify_email(request: Request, get_user: get_new_arrivals_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(get_user)
        user_list = list(get_collection_users(request).aggregate(
            [{"$match": {"user_id": getData['user_id']}}]))
        if user_list[0].get('verify_status') is None:
            update_result = get_collection_users(request).update_one({"user_id": getData['user_id']},
                                                                     {"$set": {
                                                                         "verify_status": 1
                                                                     }})
            response["error_code"] = "9999"
            response["message"] = "Successfully Verify"
        else:
            if user_list[0]['verify_status'] == 0:
                update_result = get_collection_users(request).update_one({"user_id": getData['user_id']},
                                                                         {"$set": {
                                                                             "verify_status": 1
                                                                         }})
                response["error_code"] = "9999"
                response["message"] = "Successfully Verify"
            else:

                response["error_code"] = "9998"
                response["message"] = "already Verify"

    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def otp_generate(request: Request, otp_data: Otp = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(otp_data)
        email_data = list(get_collection_users(request).aggregate(
            [{"$match": {"email": getData["email"]}}]))
        if len(email_data) > 0:
            digits = "0123456789"
            OTP = ""
            for i in range(4):
                OTP += digits[math.floor(random.random() * 10)]
            getData['otp'] = OTP
            otp_data = list(get_collection_otp(request).aggregate(
                [{"$match": {'$and': [{"email": getData["email"]}, {"type": getData["type"]}]}}]))
            if len(otp_data) > 0:
                update_result = get_collection_otp(request).update_one({"otp_id": otp_data[0]['otp_id']},
                                                                       {"$set": {
                                                                           "otp": OTP,
                                                                           "updated_date": getData["updated_date"]
                                                                       }})
                send_otp_mail(email_data[0]['email'], email_data[0]['user_name'], OTP)
                response["error_code"] = "9999"
                response["message"] = "Successfully"
            else:
                getData["otp_id"] = "otp" + str(uuid.uuid4()).replace('-', '')
                insert_result = get_collection_otp(request).insert_one(getData)
                send_otp_mail(email_data[0]['email'], email_data[0]['user_name'], OTP)
                response["error_code"] = "9999"
                response["message"] = "Successfully"
        else:
            response["error_code"] = "9998"
            response["message"] = "Email Incorrect"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


def send_otp_mail(email_to: str, user_name: str, otp: str):
    response = {}
    try:
        msg = MIMEMultipart()
        f = open(os.getcwd() + '/src/template/otptemplate.html', 'r')
        mail_content = f.read()
        mesg = "Use the following OTP to complete your Password Reset. OTP is valid for 5 minutes"
        mail_content = (mail_content.replace("##name##", user_name)
                        .replace("##msg##", mesg).replace("##otp##", otp))
        msg.attach(MIMEText(mail_content, 'html'))
        msg['Subject'] = 'OTP'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = Credantial.email_credential['password']
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(Credantial.email_credential['email'], Credantial.email_credential['password'])
            server.sendmail(Credantial.email_credential['email'], email_to, msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Email sent successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = f"Failed to send email. Error: {str(e)}"
    return response


def forget_pwd(request: Request, forget_pwd: forget_pwd_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(forget_pwd)
        email_data = list(get_collection_users(request).aggregate(
            [{"$match": {"email": getData["email"]}}]))
        if len(email_data) > 0:
            otp_data = list(get_collection_otp(request).aggregate(
                [{"$match": {'$and': [{"email": getData["email"]}, {"type": getData["type"]},
                                      {"otp": getData["otp"]}]}}]))
            if len(otp_data) > 0:
                if (datetime.strptime(otp_data[0]["updated_date"], '%Y-%m-%dT%H:%M:%S') + timedelta(
                        minutes=5) >= datetime.now()):
                    update_result = get_collection_users(request).update_one({"email": getData['email']},
                                                                             {"$set": {
                                                                                 "password": getData['password']
                                                                             }})
                    response["error_code"] = "9999"
                    response["message"] = "OTP Verify"
                else:
                    response["error_code"] = "9998"
                    response["message"] = "OTP Expire"
            else:
                response["error_code"] = "9998"
                response["message"] = "OTP Not Match"
        else:
            response["error_code"] = "9998"
            response["message"] = "Email Incorrect"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = "Error"
    return response
