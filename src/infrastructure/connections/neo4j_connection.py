import os
from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase

class Neo4jConnection:
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        if self._driver is None:
            uri = os.getenv('NEO4J_URI', 'bolt://127.0.0.1:7687')
            user = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'neo4j')
            try:
                self._driver = GraphDatabase.driver(uri, auth=(user, password))
                self._driver.verify_connectivity()
            except Exception:
                self._driver = None
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None
