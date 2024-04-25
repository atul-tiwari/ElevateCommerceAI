import requests
import json
import re

def Clean(text):
    text = text.replace("\n","").replace("\t","").replace("\r","")
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

# def get_dom_product_page(driver,url):
    
#     driver.get(url)
#     time.sleep(2)
#     driver.execute_script("window.scrollTo(0, 200)")
#     dom = lxml.html.fromstring(driver.page_source)

#     data_dict = {}
#     try:
#         tmp = ''.join(dom.xpath("//span[@id='productTitle']/text()"))
#         data_dict["Name"] = Clean(tmp)
#     except:
#         data_dict["Name"] = None

#     try:
#         tmp = ''.join(dom.xpath("(//span[@class='a-offscreen'])[1]/text()"))
#         data_dict["Price"] = Clean(tmp)
#     except:
#         data_dict["Price"] = None

#     try:
#         imgs = ''.join(dom.xpath("(//span[@class='a-offscreen'])[1]/text()"))
#         data_dict["Price"] = Clean(tmp)
#     except:
#         data_dict["Price"] = None


#     catergory = dom.xpath("//ul[contains(@class,'a-unordered-list a-horizontal')]/li/span/a/text()")
#     catergory =  list(map(Clean,catergory))
#     data_dict['Catergorys'] = catergory

#     stars = dom.xpath('//div[@role="progressbar"]/@aria-valuenow')

#     for i in range(5,0,-1):
#         data_dict[f'{i}_Stars']=stars[5-i]

#     totalRatingCount = ''.join(dom.xpath('//span[contains(@id,"acrCustomerReviewText")]/text()'))
#     data_dict["totalRatingCount"] = Clean(totalRatingCount.replace(" ratings",""))

#     rating = ''.join(dom.xpath('//span[contains(@data-hook,"rating-out-of-text")]/text()'))
#     data_dict["rating"] = Clean(rating.replace(" out of 5",""))

#     details = {}
#     tr_data = dom.xpath("//div[@id='prodDetails']//table//tr")
#     for row in tr_data:

#         key = ''.join(row.xpath("./th//text()"))
#         value = row.xpath("./td/text()")
#         details[Clean(key)] = Clean(''.join(value))
    
#     data_dict['product_details'] = details

#     print(data_dict)
#     return data_dict

def get_data_api(ASIN,API_KEY):

    params = {
    'api_key': API_KEY,
    'type': 'product',
    'asin': ASIN,
    'amazon_domain': 'amazon.com'
    }

    # make the http GET request to ASIN Data API
    api_result = requests.get('https://api.asindataapi.com/request', params)

    # print the JSON response from ASIN Data API
    data_dict = {}
    data = api_result.json()

    data_dict['title'] = data['product'].get('title')
    data_dict['link'] = data['product'].get('link')
    data_dict['categories_flat'] = data['product'].get('categories_flat')
    data_dict['rating'] = data['product'].get('rating')
    data_dict['ratings_total'] = data['product'].get('ratings_total')
    data_dict['feature_bullets'] = data['product'].get('feature_bullets')
    data_dict['attributes'] = data['product'].get('attributes')
    data_dict['specifications'] = data['product'].get('specifications')
    data_dict['bestsellers_rank'] = data['product'].get('bestsellers_rank')
    data_dict['brand'] = data['product'].get('brand')
    data_dict['description'] = data['product'].get('description')


    image_list = []

    for image in data['product'].get('images'):
        image_list.append(image.get("link"))

    return data_dict,image_list


#print(get_data_api("B07XZ8BWJX","0B403C4E89D945779874AF31D5212582"))