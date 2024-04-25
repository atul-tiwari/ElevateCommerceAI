import pandas as pd
import mysql.connector

class MySQLDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = self.connect()
    
    def connect(self):
        try:
            print(self.host,self.username,self.password,self.database)
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")
    
    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            return cursor
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def read_data(self, table_name):
        query = f"SELECT * FROM {table_name}"
        try:
            data = pd.read_sql(query, self.connection)
            return data
        except mysql.connector.Error as e:
            print(f"Error reading data from MySQL: {e}")
            return None
    
    def insert_data(self, table_name, data_dict, columns=None, values=None):
        if columns is None and values is None:
            columns = ', '.join(data_dict.keys())
            values = ', '.join([f"'{value}'" for value in data_dict.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.execute_query(query)
    
    def insert_data(self, table_name, *args):
        if len(args) == 2:
            columns, values = args
        else:
            data_dict = args[0]
            columns = ', '.join(data_dict.keys())
            values = ', '.join([f"'{value}'" for value in data_dict.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.execute_query(query)
    
    def close(self):
        self.connection.close()
        

# # Example usage
# db = MySQLDatabase(host='localhost', username='user', password='password', database='test_db')

# # Inserting data with dictionary
# data_to_insert = {'id': 1, 'name': 'John Doe', 'age': 30}
# db.insert_data('users', data_to_insert)

# # Inserting data with columns and values
# db.insert_data('users', 'id, name, age', '2, "Jane Doe", 35')
