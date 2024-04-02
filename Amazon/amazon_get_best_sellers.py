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
import pandas as pd


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

USER_AGENT=[
"edge|Mozilla/5.0 (Windows NT 10.3; x64) AppleWebKit/601.29 (KHTML, like Gecko) Chrome/52.0.3160.206 Safari/535.0 Edge/17.68023",
"chrome|Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/600.2 (KHTML, like Gecko) Chrome/55.0.2541.248 Safari/601",
"edge|Mozilla/5.0 (Windows; U; Windows NT 10.3;) AppleWebKit/603.17 (KHTML, like Gecko) Chrome/54.0.1842.208 Safari/534.4 Edge/15.74862",
"mac|Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_8) AppleWebKit/537.16 (KHTML, like Gecko) Chrome/51.0.1547.383 Safari/535",
"mac|Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_7_1; en-US) Gecko/20100101 Firefox/74.2",
"firefox|Mozilla/5.0 (Linux x86_64; en-US) Gecko/20100101 Firefox/51.8",
"windows|Mozilla/5.0 (Windows; U; Windows NT 6.0;) Gecko/20130401 Firefox/56.4",
"explorer|Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.2; x64; en-US Trident/7.0)",
"firefox|Mozilla/5.0 (Windows; Windows NT 6.0;) Gecko/20100101 Firefox/69.6",
"explorer|Mozilla/5.0 (compatible; MSIE 7.0; Windows; U; Windows NT 6.3; Trident/4.0)"
]


def get_dom(URL):
    retries = 5
    # make the request
    while retries > 0:
        
        headers["User-Agent"] = random.choice(USER_AGENT)

        try:
            # make the HTTPS request
            response = requests.get(URL, headers=headers, timeout=5)
            # if the request was successful, break out of the loop
            if response.status_code == 200:
                dom = lxml.html.fromstring(response.text)
                return dom
            else:
                raise ValueError(f"Status {response.status_code}")
        except Exception as e:
            # if there was an error, retry the request
            print("Exception : {} : {}".format(e, traceback.format_exc()))
            retries -= 1
            time.sleep(1)
            continue
    
    return None


def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text



def get_page_data(URL,page_1 = False):
    try:
        dom = get_dom(URL)

        page_no = ''.join(dom.xpath("//span[contains(@class,'s-pagination-item s-pagination-selected')]/text()"))
        category = ''.join(dom.xpath("//ul//span[contains(@class,'a-text-bold')]/text()"))

        products = dom.xpath("//div[contains(@class,'s-result-list')]/div[contains(@class,'s-result-item s-asin')]")
        products_list = []
        index = 1
        for product in products:
            try:
                _id = ''.join(product.xpath("./@data-asin"))
                name = ''.join(product.xpath(".//h2/a/span/text()"))
                try:
                    rating = ''.join(product.xpath(".//div[contains(@class,'a-row a-size-small')]/span[1]/@aria-label"))
                    rating = float(rating.replace(' 颗星，最多 5 颗星','').strip())
                except:
                    rating = None
                try:
                    no_of_rating = ''.join(product.xpath(".//div[contains(@class,'a-row a-size-small')]/span[2]/@aria-label"))
                    no_of_rating = int(str(no_of_rating).replace(',','').strip())
                except:
                    no_of_rating = None
                price  = ''.join(product.xpath(".//span[contains(@class,'a-offscreen')]//text()"))
                PPL = ''.join(product.xpath(".//span[contains(@class,'a-size-base a-color-secondary')]/text()"))

                try:
                    product_image = product.xpath(".//img[@data-image-latency='s-product-image']/@src")[0]
                except:
                    product_image = None

            except:
                pass
            data = {
                "product_id":_id,
                "name":name,
                "rating":rating,
                "no_of_rating":no_of_rating,
                "price":price,
                "PPL":PPL,
                "category":category,
                "index":index,
                "page": page_no,
                "product_image":product_image,
                # "Manufacturer":Manufacturer,
                # "Best_Selling_Ranking":Best_Selling_Ranking
            }
            index+=1
            products_list.append(data)

        try:
            if page_1:
                max_page = ''.join(dom.xpath("//span[@class='s-pagination-item s-pagination-disabled']/text()"))
                max_page = int(Clean(max_page))
            else:
                max_page =None
        except:
            max_page =None

        print(len(products_list),URL)
        time.sleep(0.2)
        return products_list,max_page
    except Exception as e:
        print("Exception : {} : {}".format(e, traceback.format_exc()))
        return [],None


def get_category_data(Cat_url):
    category_list = []
    page_no = 1
    max_page = 1
    while page_no <= max_page :
        page_url = Cat_url.format(page_no,page_no-1)
        if page_no == 1:
            products_list,max_page_ex = get_page_data(page_url,page_1=True)
            #max_page = max_page_ex
            #print(category_list[0].get("category")," Max_page =",max_page_ex)
        else:
            products_list,max_page_ex = get_page_data(page_url)

        category_list.extend(products_list)
        page_no+=1
    
    print(category_list)
    try:
        data = {"category_name":category_list[0]['category'],"category_url":Cat_url,"data":category_list}
    except:
        data = {"category_name":category_list[0]['category'],"category_url":Cat_url,"data":category_list}
    print(category_list)
    file_name =  f'{(data["category_name"]) }.pickle'
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)
    
    return max_page
    


category_list = [
'https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Basic-Cases/zgbs/wireless/3081461011/ref=zg_bs_nav_wireless_2_2407760011'
]

import concurrent.futures
if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor(1) as executor:
        futures = list(executor.map(get_category_data, category_list))
        for result in futures:
            print(result)

    product_list = []
    for _f in glob.glob(join(dirname(__file__), '*.pickle')):
        with open(_f, 'rb') as f:
            item = pickle.load(f)
            product_list.extend(item['data'])
            print(_f,len(item))
    
    data = pd.DataFrame(product_list)
    data.to_csv( join(dirname(__file__), f'Picker_data_{datetime.now().strftime("%Y%m%d")}.csv'),index=False)