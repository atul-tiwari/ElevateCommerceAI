# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Query, Request, status, Response, Header, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

import requests
import time
from contextlib import contextmanager
import os
import datetime
import sys
import random
import csv
import shutil
import re
from dotenv import load_dotenv
import pandas as pd
import numpy as np


import traceback
from loguru import logger
logger.add("./log/Amazon Site API.log", rotation="10MB", retention="1 year")

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

load_dotenv()

HOST_URL=os.getenv('HOST_URL')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
DB_NAME=os.getenv('DB_NAME')
API_KEY=os.getenv('API_KEY')
ENV=os.getenv('ENV')

from Amazon.get_key_word import get_prod_list
from Amazon.get_prod_details import get_data_api

from common.database_con import MySQLDatabase
from Amazon.API.DataTables.amazon_product_lists import amazon_product_lists
from Amazon.API.DataTables.amazon_product_details import amazon_product_details
from Amazon.API.DataTables.amazon_image_links import amazon_image_links

app = FastAPI(
    title='Amazon Site API',
    description='Control C1',
    version='0.1.5'
    #docs_url=None, 
    #redoc_url=None
)


class urldict(BaseModel):
    ASIN : str = Field(..., title="Product ID", description="unique Amazon id for Product", example= "BGCTAH2711")
    URL : str = Field(..., title="URL", description="URL", example= "https://www.amazon.com/LISEN-MagSafe-Car-Magnets-Magnetic/dp/B0BQMFGB4S?th=1")

class productListdict(BaseModel):
    type : str = Field(..., title="fetch Type", description=" cart/orders", example= "cart")
    urls : list[urldict]
    Datetime :  str = Field(..., title="datetime", description="datetime string", example= "06/10/11 15:24:16 +00:00")
    count : int = Field(..., title="product count", description="total product count", example= 5 )
    ssl_verify : bool = Field(..., title="ssl_verify", description="ssl_verify", example= True)

class product_details(BaseModel):
    ASIN : str = Field(..., title="Product ID", description="unique Amazon id for Product", example= "B0BQMFGB4S")
    tilte : str = Field(..., title="tilte", description="name", example= "LISEN-MagSafe-Car-Magnets-Magnetic")
    BASE_URL : str = Field(..., title="BASE_URL", description="URL", example= "https://www.amazon.com/LISEN-MagSafe-Car-Magnets-Magnetic/dp/B0BQMFGB4S?th=1")
    discription : str = Field(..., title="prod_desc", description="product discription", example= "")
    product_details : dict = Field(..., title="product_details", description="product details information dictonary", example= "")
    Datetime :  str = Field(..., title="datetime", description="datetime string", example= "06/10/11 15:24:16 +00:00")

class responseACK(BaseModel):
    ACK : str = Field(..., title="Acknowledgement", description="Acknowledgement", example= "Success")

def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://api.amazon.com/auth/o2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        # Handle error
        return None

    return response.json()['access_token']

def Check_auth_token(auth_token):
    try:
        tokens = open(os.path.join(sys.path[0], "auth_toknes"), "r")
        tokens = tokens.readlines()
        tokens = [tmp.replace("\n",'') for tmp in tokens]
        return auth_token in tokens
            
    except:
        return False

def connection():
    db = MySQLDatabase(host=HOST_URL, username=USER, password=PASSWORD, database=DB_NAME)
    return db
# Get_Cart : picking all products from cart
# Request : get list 
# Response : Product IDs and URLS
@app.get('/api/Get_Cart', summary="picking all products from cart", status_code=200, tags=["Get_Cart"], response_model=productListdict)
def Get_Cart(
        access_token: str = Header(..., description= "API Access Token")    
        ):
        return JSONResponse(status_code=200,content={"ACK":"Products_list"})

# Get_Cart : picking all products from orders page
# Request : get list  
# Response : Product IDs and URLS
@app.get('/api/Get_key_word', summary="picking all products from search page", status_code=200, tags=["Get_key_word"], response_model=productListdict)
def Get_key_word(
        access_token: str = Header(..., description= "API Access Token"),
        key_word: str = Header(..., description= "search keyword"),
        page_no: int = Header(..., description= "page_no"),
        ):
        if not Check_auth_token(access_token):
            return JSONResponse(status_code=500,content={"msg":"Invalid access token","access_token":access_token})
        try:
            products = get_prod_list(key_word,int(page_no))
            db = connection()
            
            insert_obj = amazon_product_lists(db.connection)
            asin_list = []
            for product in products:
                insert_obj.create_product(
                    asin=str(product['asin']),
                    product_name= str(product['product_name']),
                    url=str(product['url']),
                    keyword=str(product['keyword']),
                    rating=float(product['rating']),
                    reviews=int(product['reviews']),
                    position=int(product['position']),
                    page_no=int(product['page_no'])
                )
                asin_list.append(str(product['asin']))
            db.close()
    
        except:
            return JSONResponse(status_code=500,content={"msg":"invalid args","key_word":key_word,"page_no":page_no})

        return JSONResponse(status_code=200,content={"ACK":"Success","Prduct_added":len(asin_list),"products":asin_list})
    
# get_prod_details : picking all products details from product page
# Request : get product data 
# Response : Product IDs and URLS
@app.get('/api/get_prod_details', summary="picking all products details from product page", status_code=200, tags=["get_prod_details"], response_model=product_details)
def get_prod_details(
        access_token: str = Header(..., description= "API Access Token"),
        ASIN: str = Header(..., description= "Amazon Product ASIN")
        ):
        if not Check_auth_token(access_token):
            return JSONResponse(status_code=500,content={"msg":"Invalid access token","access_token":access_token})
        try:
            data_dict,image_list = get_data_api(ASIN,API_KEY=API_KEY)
            data_dict['asin'] = ASIN
            db = connection()
            insert_obj = amazon_product_details(db.connection)
            
            if_exists = insert_obj.read_product_details(str(data_dict['asin']))
            if if_exists is not None:
                 return JSONResponse(status_code=500,content={"msg":"Product already Exists ","asin":str(data_dict['asin'])})

            insert_obj_img = amazon_image_links(db.connection)

            pid = insert_obj.create_product_details(
                asin = str(data_dict['asin']),
                title = str(data_dict['title']),
                link  = str(data_dict['link']),
                categories_flat  = str(data_dict['categories_flat']),
                rating  = float(data_dict['rating']),
                ratings_total  = int(data_dict['ratings_total']),
                feature_bullets  = str(data_dict['feature_bullets']),
                attributes  = str(data_dict['attributes']),
                specifications  = str(data_dict['specifications']),
                bestsellers_rank  = str(data_dict['bestsellers_rank']),
                brand  = str(data_dict['brand']),
                description = str(data_dict['description'])
            )
            print(pid)
            insert_obj_img.create_image_links(image_list,str(data_dict['asin']),pid)
            db.close()
    
        except:
            return JSONResponse(status_code=500,content={"msg":"invalid args"})

        return JSONResponse(status_code=200,content={"ACK":"Products_details"})


# post_to_amazon : post all products details to amazon as new listing 
# Request : get product data 
# Response : responseACK
@app.post('/api/post_to_amazon', summary="post all products details to amazon as new listing", status_code=200, tags=["post_to_amazon"],response_model=responseACK)
def post_to_amazon(
        data : dict,
        access_token: str = Header(..., description= "API Access Token"),
        ):
        return JSONResponse(status_code=200,content={"ACK":"responseACK"}) 


@app.post('/api/post_to_ebay', summary="post all products details to ebay as new listing", status_code=200, tags=["post_to_ebay"],response_model=responseACK)
def post_to_ebay(
        data : dict,
        access_token: str = Header(..., description= "API Access Token"),
        ):
        return JSONResponse(status_code=200,content={"ACK":"responseACK"}) 



@app.get('/my-endpoint')
@app.head('/my-endpoint')
async def my_endpoint(request: Request):
    return {'status': 1, 'message': request.client.host}


if __name__ == "__main__":
    # if APP_ENV == 'local':
    #     uvicorn.run(app, host="127.0.0.1", port=8000)
    # else:
    #     uvicorn.run(app, host="0.0.0.0", port=80)
    if 

    uvicorn.run(app, host="127.0.0.1", port=8000)

    if ENV == 'DEVELOPMENT':
        uvicorn.run(app, host="127.0.0.1", port=8000)
    elif ENV == 'DEPLOY':
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        uvicorn.run(app, host="0.0.0.0", port=80)