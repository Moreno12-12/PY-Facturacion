import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from neo4j import GraphDatabase

def setup():
    uri = os.getenv('NEO4J_URI', 'bolt://127.0.0.1:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'neo4j')
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        
        session.run("""
            CREATE CONSTRAINT persona_id IF NOT EXISTS
            FOR (p:Persona) REQUIRE p.id IS UNIQUE
        """)
        
        session.run("""
            CREATE CONSTRAINT producto_id IF NOT EXISTS
            FOR (p:Producto) REQUIRE p.id IS UNIQUE
        """)
        
        print("Neo4j: Base de datos configurada con constraints.")
    
    driver.close()

if __name__ == "__main__":
    setup()
