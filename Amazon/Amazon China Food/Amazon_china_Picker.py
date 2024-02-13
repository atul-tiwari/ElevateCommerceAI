import pickle
import traceback
import requests
import random
import re
import glob
import lxml.html
import time
from USER_AGENT import USER_AGENT
from os.path import join, dirname
from datetime import datetime
import pandas as pd

id_to_country = {
    "11YSpdX38fL":"Germany",
    "11cZujJ3ygL":"USA",
    "010pElvRcOL":"UK",
    "01fbe+UjXqL":"Japan"
}

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

def get_import_country(text):
    text = text.replace(" ","").strip()
    if text == None or text == '':
        return None
    
    for key in id_to_country.keys():
        if key in text:
            return id_to_country[key]

    f = open("importCountry.txt", "a")
    f.writelines([text])
    f.close()
    return None


def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

def get_product_data(asin):
    prop_url = f"https://www.amazon.cn/dp/{asin}"
    dom = get_dom(prop_url)

    data_dict = {}
    for tr in dom.xpath("//div[@id='prodDetails']//tr"):
        key = ''.join(tr.xpath(".//th//text()"))
        value = ''.join(tr.xpath(".//td//text()"))
        data_dict[Clean(key)]=Clean(value)

    return data_dict



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
                    country_of_import = ''.join(product.xpath(".//span[contains(@class,'faceout-image-view')]/following-sibling::img/@src"))
                    country_of_import = get_import_country(country_of_import)
                except:
                    country_of_import = None

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
                "country_of_import":country_of_import,
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

        if page_1:
            max_page = ''.join(dom.xpath("//span[@class='s-pagination-item s-pagination-disabled']/text()"))
            max_page = int(Clean(max_page))
        else:
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
    while page_no <= max_page:
        page_url = Cat_url.format(page_no,page_no-1)
        if page_no == 1:
            products_list,max_page_ex = get_page_data(page_url,page_1=True)
            max_page = max_page_ex
            #print(category_list[0].get("category")," Max_page =",max_page_ex)
        else:
            products_list,max_page_ex = get_page_data(page_url)

        category_list.extend(products_list)
        page_no+=1
    try:
        data = {"category_name":category_list[0]['category'],"category_url":Cat_url,"data":category_list}
    except:
        data = {"category_name":Cat_url,"category_url":Cat_url,"data":category_list}

    file_name = join(dirname(__file__), f'{(data["category_name"]) }.pickle')
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)
    
    return max_page
    


category_list = [
"https://www.amazon.cn/s?i=grocery&rh=n%3A2141094051&fs=true&page={}&qid=1678413913&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2140457051&fs=true&page={}&qid=1678413974&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=wine&rh=n%3A43234071&fs=true&page={}&qid=1678414041&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2141095051&fs=true&page={}&qid=1678414079&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134633051&fs=true&page={}&qid=1678414489&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134644051&fs=true&page={}&qid=1678414511&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134651051&fs=true&page={}&qid=1678414528&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A1844461071&fs=true&page={}&qid=1678414586&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134669051&fs=true&page={}&qid=1678414606&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134670051&fs=true&page={}&qid=1678414627&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134675051&fs=true&page={}&qid=1678414647&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134680051&fs=true&page={}&qid=1678414663&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134691051&fs=true&page={}&qid=1678414680&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A2134701051&fs=true&page={}&qid=1678414699&ref=sr_pg_{}",
"https://www.amazon.cn/s?k=%E8%8A%82%E6%97%A5%E3%80%81%E7%A4%BC%E7%9B%92%E3%80%81%E7%A4%BC%E5%88%B8&i=grocery&rh=n%3A2134729051&page={}&c=ts&qid=1678414718&ts_id=2134729051&ref=sr_pg_{}",
"https://www.amazon.cn/s?i=grocery&rh=n%3A1538296071&fs=true&page={}&qid=1678414748&ref=sr_pg_{}"
]

import concurrent.futures
if __name__ == '__main__':

    with concurrent.futures.ThreadPoolExecutor(6) as executor:
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