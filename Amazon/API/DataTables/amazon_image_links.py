import mysql.connector
from mysql.connector import Error

class amazon_image_links:
    def __init__(self, connection):
        self.connection = connection

    def create_image_link(self, asin, product_id, link):
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO ElevateCommerceAI.amazon_image_links (asin, product_id, link)
            VALUES (%s, %s, %s)
            """
            record_to_insert = (asin, product_id, link)
            cursor.execute(insert_query, record_to_insert)
            self.connection.commit()
            print("Image link created successfully")
        except Error as e:
            print(f"Error creating image link: {e}")
    
    def create_image_links(self, links, asin, pid):
        try:
            image_links = []
            for link in links:
                image_links.append((asin,pid,link))

            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO ElevateCommerceAI.amazon_image_links (asin, product_id, link)
            VALUES (%s, %s, %s)
            """
            cursor.executemany(insert_query, image_links)
            self.connection.commit()
            print("Image links created successfully")
        except Error as e:
            print(f"Error creating image links: {e}")



    def read_image_link(self, image_id):
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT * FROM ElevateCommerceAI.amazon_image_links WHERE id = %s"
            cursor.execute(select_query, (image_id,))
            image_link = cursor.fetchone()
            if image_link:
                print("Image link details:")
                print(image_link)
            else:
                print("Image link not found")
        except Error as e:
            print(f"Error reading image link: {e}")

    def update_image_link(self, image_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            update_query = "UPDATE ElevateCommerceAI.amazon_image_links SET "
            update_values = []
            for key, value in kwargs.items():
                update_query += f"{key} = %s, "
                update_values.append(value)
            update_query = update_query.rstrip(", ") + " WHERE id = %s"
            update_values.append(image_id)
            cursor.execute(update_query, update_values)
            self.connection.commit()
            print("Image link updated successfully")
        except Error as e:
            print(f"Error updating image link: {e}")

    def delete_image_link(self, image_id):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM ElevateCommerceAI.amazon_image_links WHERE id = %s"
            cursor.execute(delete_query, (image_id,))
            self.connection.commit()
            print("Image link deleted successfully")
        except Error as e:
            print(f"Error deleting image link: {e}")
