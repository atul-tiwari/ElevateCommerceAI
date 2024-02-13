import pickle
import requests
import traceback
import random
import re
import sys
import lxml.html
import time
from USER_AGENT import USER_AGENT
import pandas as pd
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

cookies = None

proxy_list = []
for i in range(1,4):
    response = requests.get(f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page={i}&page_size=100", headers={"Authorization": "94a3056cb6e4d13ef5b61adbb44c8b99d2f9aef4"})
    data_dict = response.json()
    tmp_list = list(map(lambda x: f"http://{x['username']}:{x['password']}@{x['proxy_address']}:{x['port']}",data_dict['results']))
    proxy_list.extend(tmp_list)

def newIPNow_proxy():
    proxy = random.choice(proxy_list)
    s_proxy_dict = {"http": proxy, 'https': proxy}
    return s_proxy_dict

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","").replace("\r","").replace("\u200e","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text


def get_dom(URL):
    retries = 5
    # make the request
    while retries > 0:
        proxys = newIPNow_proxy()
        headers["User-Agent"] = random.choice(USER_AGENT)

        try:
            # make the HTTPS request
            response = requests.get(URL, headers=headers, proxies=proxys, timeout=5)
            # if the request was successful, break out of the loop
            if response.status_code == 200:
                dom = lxml.html.fromstring(response.text)
                if dom.xpath("boolean(//div[contains(@class,'s-result-list')]/div[contains(@class,'s-result-item s-asin')])") or dom.xpath("boolean(//span[@id='productTitle'])"):
                    return dom
                else:
                    raise ValueError(f"Captcha {response.status_code}")
            else:
                raise ValueError(f"Status {response.status_code}")
        except Exception as e:
            # if there was an error, retry the request
            print("Exception : {} : {}".format(e, traceback.format_exc()))
            retries -= 1
            time.sleep(1)
            continue
    
    return None

def get_product_data(ASIN):
    data_dict = {}
    data_dict['ASIN'] = ASIN
    try:
        params = {
        'ie': 'UTF8',
        'asin': ASIN,
        'ref': 'acr_search__popover',
        'contextId': 'search',
        }
        proxy = random.choice(proxy_list)
        s_proxy_dict = {"http": proxy, 'https': proxy}

        response = requests.get(
            'https://www.amazon.cn/review/widgets/average-customer-review/popover/ref=acr_search__popover',
            params=params,
            headers=headers,
            proxies=s_proxy_dict
        )
        dom = lxml.html.fromstring(response.text)
        data_dict = {}
        data_dict['ASIN'] = ASIN
        stars = dom.xpath('//div[@role="progressbar"]/@aria-valuenow')

        for i in range(5,0,-1):
            data_dict[f'{i}_Stars']=stars[5-i]

        totalRatingCount = dom.xpath('//span[contains(@class,"totalRatingCount")]/text()')[0]
        data_dict["totalRatingCount"] = Clean(totalRatingCount.replace("买家评级",""))

        rating = dom.xpath('//span[contains(@data-hook,"acr-average")]/text()')[0]
        data_dict["rating"] = Clean(rating.replace("星，共 5 星",""))
    except Exception as e:
        data_dict['product_details'] = e
    return data_dict



def save_data(data_list,error_asin):
    pd.DataFrame(data_list).to_csv( join(dirname(__file__), f'Crawl_stars_{datetime.now().strftime("%Y%m%d")}.csv'),index=False)
    
    with open("error_asin.txt", "a") as file:
        for line in error_asin:
            file.write(line + "\n")

import concurrent.futures

if __name__ == '__main__':

    file_name = str(sys.argv[1])
    
    error_asin = []

    data_asin = pd.read_csv(file_name)
    asin_list = list(data_asin['product_id'])


    data_list =[]

    with concurrent.futures.ThreadPoolExecutor(2) as executor:
        futures = list(executor.map(get_product_data, asin_list))
        for result in futures:
            data_list.append(result)

    save_data(data_list=data_list,error_asin=error_asin)
