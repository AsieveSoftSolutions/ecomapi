import os
import uuid
from typing import List
from fastapi import APIRouter, Body, Request, status, UploadFile
import src.config.credential as Credantial
from fastapi.responses import FileResponse
import razorpay
from src.models.custom_model import response_return_model, get_orderid_request,refund_request_data
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime,timedelta
router = APIRouter(prefix="/file", tags=["file"])


@router.post("/upload_files")
def file_contents(files: List[UploadFile]):
    response = {}
    try:
        isExist = os.path.exists(Credantial.user_file_upload_path)
        if not isExist:
            os.makedirs(Credantial.user_file_upload_path)

        ListFiles = files
        file_name = []
        for item in ListFiles:
            fileName1 = item.filename.split('.')[0]
            fileName = str(uuid.uuid4()) + '_' + fileName1.split(' ')[0] + '.' + item.filename.split('.')[-1]
            file_path = os.path.join(Credantial.user_file_upload_path, fileName)
            with open(file_path, 'wb') as f:
                f.write(item.file.read())
            file_name.append(fileName)

        response["error_code"] = "9999"
        response["message"] = "Successfully"
        response["data"] = file_name
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = str(e)
    return response


@router.delete('/delete_file/{file_name}')
def delete_file(file_name):
    response = {}
    try:
        file_path = os.path.join(Credantial.user_file_upload_path, file_name)
        os.remove(file_path)
        response["error_code"] = "9999"
        response["message"] = "Successfully Remove Image"
    except Exception as e:
        response["error_code"] = "9998"
        response["message"] = str(e)
    return response


@router.get('/view_upload_file/{file_name}')
def view_upload_file(file_name):
    try:
        isExist = os.path.exists(Credantial.user_file_upload_path + file_name)
        if isExist:
            return FileResponse(Credantial.user_file_upload_path + file_name)
        else:
            return FileResponse(Credantial.user_file_upload_path + "user_aveter.png")
    except Exception as e:
        return str(e)


@router.post('/rezorpay_order', response_description="Create a new user", status_code=status.HTTP_201_CREATED,
             response_model=response_return_model)
def razorpay_order(orderData: get_orderid_request = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(orderData)
        client = razorpay.Client(auth=(Credantial.razor_pay_key, Credantial.razor_pay_secret_key))

        DATA = getData
        data = client.order.create(data=DATA)
        getOrderData = {k: v for k, v in data.items() if v is not None}  # loop in the dict
        listData = []
        listData.append(getOrderData)
        response["error_code"] = "9999"
        response["message"] = "Successfully OrderId Create"
        response["data"] = listData
    except Exception as e:
        response["error_code"] = "9998"
        response["message"] = str(e)
    return response


@router.post('/razorpay_refund_amount', response_description="Create a new user", status_code=status.HTTP_201_CREATED,
             response_model=response_return_model)
def razorpay_refund(orderData: refund_request_data = Body(...)):
    response = {}
    try:
        getData = jsonable_encoder(orderData)
        client = razorpay.Client(auth=(Credantial.razor_pay_key, Credantial.razor_pay_secret_key))

        DATA = getData
        data = client.payment.refund(getData['payment_id'], {
            "amount": getData['amount'],
            "speed": "optimum",
            "notes": {
                "notes_key_1": "Beam me up Scotty.",
                "notes_key_2": "Engage"
            },
            "receipt": "Receipt No. "+datetime.now().strftime("%d%m%y%H%M%S%f")
        })
        getOrderData = {k: v for k, v in data.items() if v is not None}  # loop in the dict
        listData = []
        listData.append(getOrderData)
        response["error_code"] = "9999"
        response["message"] = "Successfully refund Create"
        response["data"] = listData
    except Exception as e:
        response["error_code"] = "9998"
        response["message"] = str(e)
    return response


@router.post('/email_send/{email_to}', response_description="Create a new user", status_code=status.HTTP_201_CREATED,
             response_model=response_return_model)
def send_verify_mail(email_to: str):
    response = {}
    try:
        msg = MIMEMultipart()
        f = open(os.getcwd() + '/src/template/verifyemail.html', 'r')
        mail_content = f.read()
        mail_content = (mail_content.replace("##name##", 'gopi')
                        .replace("##link##", 'https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server'))

        msg.attach(MIMEText(mail_content, 'html'))
        sender_email = "theeran@avelator.com"
        sender_password = "ekfq aaoh kmcl kwav"
        msg['Subject'] = 'mail'
        msg['From'] = Credantial.email_credential['email']
        msg['To'] = Credantial.email_credential['password']
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_to, msg.as_string())
        response["error_code"] = "9999"
        response["message"] = "Email sent successfully"
    except Exception as e:
        response["error_code"] = "0000"
        response["message"] = f"Failed to send email. Error: {str(e)}"
    return response


