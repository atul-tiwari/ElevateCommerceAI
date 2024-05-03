import mysql.connector
from mysql.connector import Error

class amazon_product_lists:
    def __init__(self, connection):
        self.connection = connection

    def create_product(self, asin, product_name, url, keyword, rating, reviews, position, page_no):
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO ElevateCommerceAI.amazon_product_lists (asin,product_name,url,keyword,rating,reviews,`position`,page_no)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert = (asin, product_name, url, keyword, rating, reviews, position, page_no)
            cursor.execute(insert_query, record_to_insert)
            self.connection.commit()
            print("Product created successfully")
        except Error as e:
            print(f"Error creating product: {e}")

    def read_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT * FROM sys.amazon_product_lists WHERE id = %s"
            cursor.execute(select_query, (product_id,))
            product = cursor.fetchone()
            if product:
                print("Product details:")
                print(product)
            else:
                print("Product not found")
        except Error as e:
            print(f"Error reading product: {e}")

    def update_product(self, product_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            update_query = "UPDATE sys.amazon_product_lists SET "
            update_values = []
            for key, value in kwargs.items():
                update_query += f"{key} = %s, "
                update_values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE id = %s"
            update_values.append(product_id)
            cursor.execute(update_query, update_values)
            self.connection.commit()
            print("Product updated successfully")
        except Error as e:
            print(f"Error updating product: {e}")

    def delete_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM sys.amazon_product_lists WHERE id = %s"
            cursor.execute(delete_query, (product_id,))
            self.connection.commit()
            print("Product deleted successfully")
        except Error as e:
            print(f"Error deleting product: {e}")
