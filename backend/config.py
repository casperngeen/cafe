import mysql.connector

class DbConfig:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'yourpassword'
    MYSQL_DB = 'cafesystem'

    # Establishing MySQL connection
    @staticmethod
    def get_db_connection():
        connection = mysql.connector.connect(
            host=DbConfig.MYSQL_HOST,
            user=DbConfig.MYSQL_USER,
            password=DbConfig.MYSQL_PASSWORD,
            database=DbConfig.MYSQL_DB
        )
        return connection