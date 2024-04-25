import mysql.connector
from mysql.connector import Error

class amazon_product_details:
    def __init__(self, connection):
        self.connection = connection

    def create_product_details(self, asin, title, link, categories_flat, rating, ratings_total, feature_bullets, attributes, specifications, bestsellers_rank, brand, description):
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO ElevateCommerceAI.amazon_product_details (asin, title, link, categories_flat, rating, ratings_total, feature_bullets, attributes, specifications, bestsellers_rank, brand, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert = (asin, title, link, categories_flat, rating, ratings_total, feature_bullets, attributes, specifications, bestsellers_rank, brand, description)
            cursor.execute(insert_query, record_to_insert)
            self.connection.commit()
            print("Product details created successfully")

            cursor.execute('select last_insert_id()')
            return cursor.fetchone()[0]
        except Error as e:
            print(f"Error creating product details: {e}")
            return None

    def read_product_details(self, ASIN):
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT * FROM ElevateCommerceAI.amazon_product_details WHERE asin = %s"
            cursor.execute(select_query, (ASIN,))
            product_details = cursor.fetchone()
            if product_details:
                #print("Product details:")
                return product_details
            else:
                print("Product details not found")
                return None
        except Error as e:
            print(f"Error reading product details: {e}")
            return None

    def update_product_details(self, product_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            update_query = "UPDATE ElevateCommerceAI.amazon_product_details SET "
            update_values = []
            for key, value in kwargs.items():
                update_query += f"{key} = %s, "
                update_values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE id = %s"
            update_values.append(product_id)
            cursor.execute(update_query, update_values)
            self.connection.commit()
            print("Product details updated successfully")
        except Error as e:
            print(f"Error updating product details: {e}")

    def delete_product_details(self, product_id):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM ElevateCommerceAI.amazon_product_details WHERE id = %s"
            cursor.execute(delete_query, (product_id,))
            self.connection.commit()
            print("Product details deleted successfully")
        except Error as e:
            print(f"Error deleting product details: {e}")

