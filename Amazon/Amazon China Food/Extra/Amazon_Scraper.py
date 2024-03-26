import lxml.html
import json,traceback,re
from amazoncaptcha import AmazonCaptcha
from selenium_settings import selenium_get_dom

id_to_country = {
    "11YSpdX38fL":"Germany",
    "11cZujJ3ygL":"USA",
    "010pElvRcOL":"UK",
    "01fbe+UjXqL":"Japan"
}



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

def get_page_data(driver,URL):
    try:
        dom = selenium_get_dom(driver,URL)
        #captcha Check 
        if dom.xpath("boolean(//h4[contains(.,'Enter the characters you see below')])") == 1:   
            captcha = AmazonCaptcha.from_webdriver(driver)
            solution = captcha.solve()
            captcha_filed = driver.find_element_by_xpath("//input[@id='captchacharacters']")
            captcha_filed.send_keys(solution)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            HTML = driver.find_element_by_xpath("//body").get_attribute("innerHTML")
            dom = lxml.html.fromstring(HTML)

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


                # try:
                #     product_data,image = get_product_data(driver,_id)
                #     #product_image = image
                #     Manufacturer =  product_data.get("制造商",None)
                #     Best_Selling_Ranking = product_data.get("亚马逊热销商品排名",None)
                # except Exception as e:
                #     Manufacturer,Best_Selling_Ranking,product_image = None,None,None
                #     print("Exception : {} : {}".format(e, traceback.format_exc()))

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
            }
            index+=1
            products_list.append(data)
        try:
            next_page = product.xpath("//a[contains(@class,'s-pagination-next')]/@href")[0]
            next_page = "https://www.amazon.cn"+next_page
        except:
            next_page = None
        
        return products_list,next_page
    except Exception as e:
        print("Exception : {} : {}".format(e, traceback.format_exc()))
        return [],None


def get_category_data(driver,Cat_url):
    category_list = []
    page_url = Cat_url
    while True:
        products_list,next_page_url = get_page_data(driver,page_url)
        category_list.append(products_list)
        print(len(products_list),Cat_url,products_list)
        if next_page_url is None:
            break
        else:
            page_url = next_page_url
    return category_list
