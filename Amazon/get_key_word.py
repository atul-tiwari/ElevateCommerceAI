import pickle
import traceback
import requests
import random
import re
import glob
import lxml.html
import time
from os.path import join, dirname
from datetime import datetime

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.amazon.cn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'downlink': '6.85',
    'ect': '4g',
    'rtt': '100',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
}

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

def get_prod_list(keyword,page_no):

    _url  = f"https://www.amazon.com/s?k={keyword}&page={page_no}&ref=sr_pg_{page_no}"

    try:
        res = requests.get(_url, headers=headers, proxies={}, timeout=5)
        dom = lxml.html.fromstring(res.text)

        products = dom.xpath("//div[contains(@data-component-type,'s-search-result')]")

        data_list = []
        for product in products:
            data_dict ={}
            try:
                data_dict['asin'] = product.xpath("./@data-asin")[0]
            except:
                data_dict['asin'] = None
            
            try:
                data_dict['product_name'] = Clean(''.join(product.xpath(".//h2//text()")))
            except:
                data_dict['product_name'] = None
            
            try:
                data_dict['url'] = f"https://www.amazon.com//dp/{data_dict['asin']}/"
            except:
                data_dict['url'] = None
            
            try:
                data_dict['keyword'] = keyword
            except:
                data_dict['keyword'] = None
            
            try:
                tmp = Clean(''.join(product.xpath(".//i/span/text()")))
                tmp = tmp.replace(" out of 5 stars","")
                data_dict['rating'] = float(tmp)
            except:
                data_dict['rating'] = None
            
            try:
                tmp = Clean(''.join(product.xpath(".//div[contains(@class,'instrumentation-wrapper')]//text()")))
                tmp = tmp.replace(',','')
                tmp = int(tmp)
                data_dict['reviews'] = tmp
            except:
                data_dict['reviews'] = None

            try:
                data_dict['position'] = int(product.xpath("./@data-index")[0])
            except:
                data_dict['position'] = None
            
            try:
                data_dict['page_no'] = page_no
            except:
                data_dict['page_no'] = None
            
            data_list.append(data_dict)
        
        return data_list

    except: 
        print("Exception : {} : {}".format(e, traceback.format_exc()))
        return -1
    

get_prod_list("charger",1)
    
