from fastapi import FastAPI
import uvicorn
from dotenv import dotenv_values
from pymongo import MongoClient
from routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
config = dotenv_values(".env")

app = FastAPI()


config = dotenv_values(".env")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("mongodb+srv://sengunthar:zse45rdx%40123@cluster0.5ix5svx.mongodb.net/")
    app.database = app.mongodb_client["eCommerce"]
    # app.mongodb_client = MongoClient("mongodb+srv://cmsAdmin:cmsadmin123@cluster0.k0hsbae.mongodb.net/")
    # app.database = app.mongodb_client["ecommerce_stg"]
    print("Project connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(api_router)

if __name__ == '__main__': #this indicates that this a script to be run
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)








