import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from cassandra.io.asyncioreactor import AsyncioConnection
sys.modules['cassandra.io.asyncorereactor'] = type(sys)('fake_asyncore')
sys.modules['cassandra.io.asyncorereactor'].AsyncoreConnection = AsyncioConnection

from cassandra.cluster import Cluster

def setup():
    host = os.getenv('CASSANDRA_HOST', '127.0.0.1')
    keyspace = os.getenv('CASSANDRA_KEYSPACE', 'freshmart')
    
    cluster = Cluster([host], connection_class=AsyncioConnection)
    session = cluster.connect()
    
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
    """)
    
    session.set_keyspace(keyspace)
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id UUID PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            tipo TEXT,
            email TEXT,
            telefono TEXT,
            barrio TEXT,
            municipio TEXT,
            edad INT,
            estrato INT
        )
    """)
    
    print("Cassandra: Keyspace y tabla 'personas' creados correctamente.")
    cluster.shutdown()

if __name__ == "__main__":
    setup()
