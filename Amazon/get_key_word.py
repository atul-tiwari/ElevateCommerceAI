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

user_agents = [

'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'

]

proxy = {"http": 'http://vozxnovu:aufihbhunt1n@157.52.145.169:5778', 'https': 'http://vozxnovu:aufihbhunt1n@157.52.145.169:5778'}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.amazon.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': random.choice(user_agents),
}

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

def get_prod_list(keyword,page_no):
    response = requests.get('https://www.amazon.com/')
    cookies = response.cookies
    _url  = f"https://www.amazon.com/s?k={keyword}&page={page_no}"

    try:
        res = requests.get(_url, headers=headers, timeout=5, cookies=cookies)
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
                data_dict['url'] = f"https://www.amazon.com/dp/{data_dict['asin']}/"
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

    except Exception as e: 
        print("Exception : {} : {}".format(e, traceback.format_exc()))
        return -1
    
if __name__ == "__main__":
    print(get_prod_list("charger",1))