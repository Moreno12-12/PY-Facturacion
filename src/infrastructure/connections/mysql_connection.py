import os
from dotenv import load_dotenv

load_dotenv()

import mysql.connector

class MySQLConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            config = {
                'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
                'port': int(os.getenv('MYSQL_PORT', 3306)),
                'user': os.getenv('MYSQL_USER', 'root'),
                'password': os.getenv('MYSQL_PASSWORD', ''),
                'database': os.getenv('MYSQL_DB', 'freshmart'),
            }
            self._connection = mysql.connector.connect(**config)
        return self._connection

    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None
