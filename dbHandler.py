import psycopg2
from datetime import datetime

class DBHandler:
    def __init__(self, host, port, dbname, user, password):
        self.db_host = host
        self.db_port = port
        self.db_name = dbname
        self.db_user = user
        self.db_password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            print("Connected to the database successfully!")
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def insert_data(self, id, name, price, insurance_type,email):
        print("here")
        try:
            print("here 2")
            cursor = self.connection.cursor()
            query = "INSERT INTO salesDate (id, name, price, insurance_type, email, date) VALUES (%s, %s, %s, %s, %s, %s)"
            created_at = datetime.now()
            print(created_at)
            cursor.execute(query, (id, name, price, insurance_type,email,created_at))
            self.connection.commit()
            cursor.close()
            print("Data inserted successfully!")
        except psycopg2.Error as e:
            print("Error inserting data:", e)

    def sum_sales_per_email(self, email):
        try:
            cursor = self.connection.cursor()
            query = "SELECT SUM(price) FROM salesDate WHERE email = %s;"
            cursor.execute(query, (email,))
            sum_price = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return sum_price
        except psycopg2.Error as e:
            print("Error sum data:", e)
