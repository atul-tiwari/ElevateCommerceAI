import pickle
import requests
import traceback
import random
import re
import sys
import lxml.html
import time
from USER_AGENT import USER_AGENT
from selenium_settings import selenium_get_dom,get_Driver
from datetime import datetime

headers = {
    'Accept': 'text/html,*/*',
    'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'downlink': '2.1',
    'ect': '4g',
    'rtt': '100',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
}

response = requests.get(f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page={random.randint(1,5)}&page_size=50", headers={"Authorization": "94a3056cb6e4d13ef5b61adbb44c8b99d2f9aef4"})
data_dict = response.json()
proxy_list = list(map(lambda x: f"http://{x['username']}:{x['password']}@{x['proxy_address']}:{x['port']}",data_dict['results']))
def newIPNow_proxy():
    proxy = random.choice(proxy_list)
    s_proxy_dict = {"http": proxy, 'https': proxy}
    return s_proxy_dict

def save_data(data_list,error_asin):
    with open(f'asin_data_list_{int(sys.argv[1])}-{int(sys.argv[2])}.data', 'wb') as f:
        pickle.dump(data_list, f)
    
    # with open("error_asin.txt", "a") as file:
    #     for line in error_asin:
    #         file.write(line + "\n")

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
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

def get_product_data(driver,ASIN):
    data_dict = {}
    data_dict['ASIN'] = ASIN

    #dom = selenium_get_dom(driver,f"https://www.amazon.cn/dp/{ASIN}/")
    dom = get_dom(f"https://www.amazon.cn/dp/{ASIN}/")
    catergory = dom.xpath("//ul[contains(@class,'a-unordered-list a-horizontal')]/li/span/a/text()")
    catergory =  list(map(Clean,catergory))
    data_dict['Catergorys'] = catergory

    stars = dom.xpath('//div[@role="progressbar"]/@aria-valuenow')

    for i in range(5,0,-1):
        data_dict[f'{i}_Stars']=stars[5-i]

    totalRatingCount = ''.join(dom.xpath('//span[contains(@id,"acrCustomerReviewText")]/text()'))
    data_dict["totalRatingCount"] = Clean(totalRatingCount.replace("买家评级",""))

    rating = ''.join(dom.xpath('//span[contains(@data-hook,"rating-out-of-text")]/text()'))
    data_dict["rating"] = Clean(rating.replace("星，共 5 星",""))

    details = {}
    tr_data = dom.xpath("//div[@id='prodDetails']//table//tr")
    for row in tr_data:

        key = ''.join(row.xpath("./th//text()"))
        value = row.xpath("./td/text()")
        details[Clean(key)] = Clean(''.join(value))
    
    data_dict['product_details'] = details
    return data_dict



if __name__ == '__main__':


    with open(r'H:\w_crawler\Amazon China Food\r_asin_list.pickle', 'rb') as f:
        asin_list = pickle.load(f)

    error_asin = []

    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        asin_list = asin_list[start:end]
    except:
        print("invalid Arguments")
        sys.exit()

    data_list =[]

    #driver = get_Driver({})

    for asin in asin_list:
        try:
            len_data_list = len(data_list)
            asin_data = get_product_data({},asin)
            data_list.append(asin_data)

            curent_date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curent_date_time} {len_data_list} of {len(asin_list)} done ASIN = {asin} , {len(asin_data)}")
            
        except Exception as e:
            error_asin.append(asin)

        if len_data_list % 50 == 0:
            save_data(data_list=data_list,error_asin=error_asin)

    save_data(data_list=data_list,error_asin=error_asin)