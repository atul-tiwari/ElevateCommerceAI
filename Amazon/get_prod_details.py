from Amazon import selenium_get_dom
from selenium.webdriver.common.by import By
import time
import lxml.html
import re

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

def get_dom_product_page(driver,url):
    
    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 200)")
    dom = lxml.html.fromstring(driver.page_source)

    data_dict = {}
    try:
        tmp = ''.join(dom.xpath("//span[@id='productTitle']/text()"))
        data_dict["Name"] = Clean(tmp)
    except:
        data_dict["Name"] = None

    try:
        tmp = ''.join(dom.xpath("(//span[@class='a-offscreen'])[1]/text()"))
        data_dict["Price"] = Clean(tmp)
    except:
        data_dict["Price"] = None

    try:
        imgs = ''.join(dom.xpath("(//span[@class='a-offscreen'])[1]/text()"))
        data_dict["Price"] = Clean(tmp)
    except:
        data_dict["Price"] = None


    catergory = dom.xpath("//ul[contains(@class,'a-unordered-list a-horizontal')]/li/span/a/text()")
    catergory =  list(map(Clean,catergory))
    data_dict['Catergorys'] = catergory

    stars = dom.xpath('//div[@role="progressbar"]/@aria-valuenow')

    for i in range(5,0,-1):
        data_dict[f'{i}_Stars']=stars[5-i]

    totalRatingCount = ''.join(dom.xpath('//span[contains(@id,"acrCustomerReviewText")]/text()'))
    data_dict["totalRatingCount"] = Clean(totalRatingCount.replace(" ratings",""))

    rating = ''.join(dom.xpath('//span[contains(@data-hook,"rating-out-of-text")]/text()'))
    data_dict["rating"] = Clean(rating.replace(" out of 5",""))

    details = {}
    tr_data = dom.xpath("//div[@id='prodDetails']//table//tr")
    for row in tr_data:

        key = ''.join(row.xpath("./th//text()"))
        value = row.xpath("./td/text()")
        details[Clean(key)] = Clean(''.join(value))
    
    data_dict['product_details'] = details

    print(data_dict)
    return data_dict