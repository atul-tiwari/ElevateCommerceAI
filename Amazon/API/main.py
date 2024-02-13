# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Query, Request, status, Response, Header, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

import json
import time
from contextlib import contextmanager
import os
import datetime
import sys
import random
import csv
import shutil
import re

import pandas as pd
import numpy as np

import traceback
from loguru import logger
logger.add("./log/Amazon Site API.log", rotation="10MB", retention="1 year")

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

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


# Get_Cart : picking all products from cart
# Request : get list 
# Response : Product IDs and URLS
@app.get('/api/Get_Cart', summary="picking all products from cart", status_code=200, tags=["Get_Cart"], response_model=productListdict)
def PickPolling(
        access_token: str = Header(..., description= "API Access Token")    
        ):
        return JSONResponse(status_code=200,content={"ACK":"Products_list"})

# Get_Cart : picking all products from orders page
# Request : get list  
# Response : Product IDs and URLS
@app.get('/api/Get_Orders', summary="picking all products from orders page", status_code=200, tags=["Get_Orders"], response_model=productListdict)
def PickPolling(
        access_token: str = Header(..., description= "API Access Token")    
        ):
        return JSONResponse(status_code=200,content={"ACK":"Products_list"})
    
# get_prod_details : picking all products details from product page
# Request : get product data 
# Response : Product IDs and URLS
@app.get('/api/get_prod_details', summary="picking all products details from product page", status_code=200, tags=["get_prod_details"], response_model=product_details)
def PickPolling(
        access_token: str = Header(..., description= "API Access Token"),
        _url: str = Header(..., description= "Amazon Product URL")
        ):
        return JSONResponse(status_code=200,content={"ACK":"Products_details"})


# post_to_amazon : post all products details to amazon as new listing 
# Request : get product data 
# Response : responseACK
@app.post('/api/post_to_amazon', summary="post all products details to amazon as new listing", status_code=200, tags=["post_to_amazon"],response_model=responseACK)
def object_storage(
        data : dict,
        access_token: str = Header(..., description= "API Access Token"),
        ):
        return JSONResponse(status_code=200,content={"ACK":"responseACK"}) 



@app.get('/my-endpoint')
@app.head('/my-endpoint')
async def my_endpoint(request: Request):
    return {'status': 1, 'message': request.client.host}


if __name__ == "__main__":
    if APP_ENV == 'local':
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        uvicorn.run(app, host="0.0.0.0", port=80)