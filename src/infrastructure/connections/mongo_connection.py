import os
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient

class MongoConnection:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        if self._db is None:
            host = os.getenv('MONGO_HOST', '127.0.0.1')
            port = int(os.getenv('MONGO_PORT', 27017))
            db_name = os.getenv('MONGO_DB', 'freshmart')
            self._client = MongoClient(host=host, port=port)
            self._db = self._client[db_name]
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
