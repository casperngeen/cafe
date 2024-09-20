import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
db_host = os.getenv('MYSQL_HOST')
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db = os.getenv('MYSQL_DATABASE')

class DbConfig:
    # Establishing MySQL connection
    @staticmethod
    def get_db_connection():
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db,
        )
        return connection