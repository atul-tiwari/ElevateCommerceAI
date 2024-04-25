from common.database_con import MySQLDatabase

db = MySQLDatabase(host='database-eval.c9ic26sggw0l.us-east-2.rds.amazonaws.com', username='admin', password='NoLr9415wf9F', database='ElevateCommerceAI')

#con = db.connect()

print(db.read_data("amazon_product_lists"))
from Amazon.API.DataTables.amazon_product_lists import amazon_product_lists
insert_obj = amazon_product_lists(db.connection)

insert_obj.create_product(
                    asin="sdkjnfjsk76",
                    product_name= "ABCDEFGH",
                    url="ABC.com",
                    keyword="a",
                    rating=4.5,
                    reviews=500,
                    position=78,
                    page_no=4
                )