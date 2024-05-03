from common.database_con import MySQLDatabase

db = MySQLDatabase(host='database-eval.c9ic26sggw0l.us-east-2.rds.amazonaws.com', username='admin', password='NoLr9415wf9F', database='ElevateCommerceAI')

#con = db.connect()

from Amazon.API.DataTables.amazon_product_details import amazon_product_details
insert_obj = amazon_product_details(db.connection)

print(insert_obj.read_product_details("B07XZFGHWJX"))

# import json
# data_dict = """ 
# {
#  "asin":"B07XZ8BWJX",
#   "title": "GANNOU Men's Air Athletic Running Shoes Fashion Sport Gym Jogging Tennis Fitness Sneaker (US 7-12.5) 10.5 Darkblue",
#   "link": "https://www.amazon.com/dp/B07XZ8BWJX??th=1&psc=1",
#   "categories_flat": "All Departments > Clothing, Shoes & Jewelry > Men > Shoes > Athletic > Running > Road Running",
#   "rating": 4.2,
#   "ratings_total": 3713,
#   "feature_bullets": [
#     "Air Cushion Design: it delivers a soft, smooth and responsive ride. Men tennis shoes helps evenly disperse impact to provide a smooth transition and soft feel.",
#     "Breathable Fabric Upper: Knit construction provides lightweight flexibility and breathability. Athletic shoes for men is great and very light for running.",
#     "Injection Eyelet Design: alternating formation of lace eye row created for better fit. Men running shoes with a top eyelet provide enhanced lock down.it is strong and durable.",
#     "Inspired Designs: Geometric,athlete-informed outsole pattern helps evenly disperse impact to provide a smooth transition and soft feel. Gym shoes is very comfortable for your feet.",
#     "Size: it fits just right. Sport shoes for men also has great arch support and super soft. Overall great shoe. Good fit, solid amount of cushion and hip look."
#   ],
#   "attributes": [
#     {
#       "name": "size",
#       "value": "10.5"
#     },
#     {
#       "name": "color",
#       "value": "Darkblue"
#     }
#   ],
#   "specifications": [
#     {
#       "name": "Product Dimensions",
#       "value": "11.81 x 3.15 x 3.94 inches; 14.11 ounces"
#     },
#     {
#       "name": "Department",
#       "value": "mens"
#     },
#     {
#       "name": "Date First Available",
#       "value": "September 17, 2019"
#     },
#     {
#       "name": "ASIN",
#       "value": "B07XZ7HHP6"
#     },
#     {
#       "name": "Best Sellers Rank",
#       "value": "See Top 100 in Clothing, Shoes & Jewelry"
#     },
#     {
#       "name": "Origin",
#       "value": "Imported"
#     },
#     {
#       "name": "Sole material",
#       "value": "Rubber"
#     },
#     {
#       "name": "Platform height",
#       "value": ".50"
#     },
#     {
#       "name": "Outer material",
#       "value": "Knit"
#     },
#     {
#       "name": "Country of Origin",
#       "value": "China"
#     }
#   ],
#   "bestsellers_rank": [
#     {
#       "category": "Clothing, Shoes & Jewelry",
#       "rank": 316807,
#       "link": "https://www.amazon.com/gp/bestsellers/fashion/ref=pd_zg_ts_fashion"
#     },
#     {
#       "category": "Men's Road Running Shoes",
#       "rank": 857,
#       "link": "https://www.amazon.com/gp/bestsellers/fashion/14210389011/ref=pd_zg_hrsr_fashion"
#     }
#   ],
#   "brand": "GANNOU",
#   "description": null
# }


#  """ 
# data_dict = json.loads(str(data_dict))

# print(insert_obj.create_product_details(
#     asin = str(data_dict['asin']),
#     title = str(data_dict['title']),
#     link  = str(data_dict['link']),
#     categories_flat  = str(data_dict['categories_flat']),
#     rating  = float(data_dict['rating']),
#     ratings_total  = int(data_dict['ratings_total']),
#     feature_bullets  = str(data_dict['feature_bullets']),
#     attributes  = str(data_dict['attributes']),
#     specifications  = str(data_dict['specifications']),
#     bestsellers_rank  = str(data_dict['bestsellers_rank']),
#     brand  = str(data_dict['brand']),
#     description = str(data_dict['description'])
# ))