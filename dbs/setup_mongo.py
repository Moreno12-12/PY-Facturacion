import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

def setup():
    host = os.getenv('MONGO_HOST', '127.0.0.1')
    port = int(os.getenv('MONGO_PORT', 27017))
    db_name = os.getenv('MONGO_DB', 'freshmart')
    
    client = MongoClient(host=host, port=port)
    db = client[db_name]
    
    db.create_collection("productos")
    
    db.productos.create_index("nombre")
    db.productos.create_index("categoria")
    db.productos.create_index("tags")
    
    print("MongoDB: Coleccion 'productos' creada correctamente.")
    client.close()

if __name__ == "__main__":
    setup()
