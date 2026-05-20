import os
from dotenv import load_dotenv

load_dotenv()

import sys
from cassandra.io.asyncioreactor import AsyncioConnection
sys.modules['cassandra.io.asyncorereactor'] = type(sys)('fake_asyncore')
sys.modules['cassandra.io.asyncorereactor'].AsyncoreConnection = AsyncioConnection

from cassandra.cluster import Cluster

class CassandraConnection:
    _instance = None
    _cluster = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self, keyspace: str = None):
        if self._session is None:
            host = os.getenv('CASSANDRA_HOST', '127.0.0.1')
            self._cluster = Cluster([host], connection_class=AsyncioConnection)
            if keyspace:
                self._session = self._cluster.connect(keyspace)
            else:
                self._session = self._cluster.connect()
        return self._session

    def close(self):
        if self._cluster:
            self._cluster.shutdown()
            self._cluster = None
            self._session = None
