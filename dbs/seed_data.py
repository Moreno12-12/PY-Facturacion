import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

import uuid
import time
from datetime import datetime

# Cassandra
from cassandra.io.asyncioreactor import AsyncioConnection
sys.modules['cassandra.io.asyncorereactor'] = type(sys)('fake_asyncore')
sys.modules['cassandra.io.asyncorereactor'].AsyncoreConnection = AsyncioConnection
from cassandra.cluster import Cluster
from cassandra.util import uuid_from_time

# MongoDB
from pymongo import MongoClient

# MySQL
import mysql.connector

# Neo4j
from neo4j import GraphDatabase

def _obtener_rango_edad(edad):
    if edad is None:
        return "desconocido"
    if edad < 18:
        return "menor_18"
    elif edad < 25:
        return "18_24"
    elif edad < 35:
        return "25_34"
    elif edad < 45:
        return "35_44"
    elif edad < 55:
        return "45_54"
    elif edad < 65:
        return "55_64"
    else:
        return "65_plus"

def seed_all():
    print("=" * 50)
    print("Cargando datos de prueba en todas las bases de datos...")
    print("=" * 50)
    
    seed_cassandra()
    seed_mongo()
    seed_mysql()
    seed_neo4j()
    
    print("=" * 50)
    print("Datos cargados correctamente en todas las bases de datos.")
    print("=" * 50)

def seed_cassandra():
    print("\n[Cassandra] Insertando personas...")
    host = os.getenv('CASSANDRA_HOST', '127.0.0.1')
    keyspace = os.getenv('CASSANDRA_KEYSPACE', 'freshmart')
    
    cluster = Cluster([host], connection_class=AsyncioConnection)
    session = cluster.connect(keyspace)
    
    session.execute("TRUNCATE personas")
    
    personas = [
        ("cliente", "Carlos", "Martinez", "carlos@email.com", "3001234567", "El Prado", "Barranquilla", 28, 4),
        ("cliente", "Ana", "Lopez", "ana@email.com", "3009876543", "Alto Prado", "Barranquilla", 32, 5),
        ("cliente", "Pedro", "Gomez", "pedro@email.com", "3005551234", "Villa Santos", "Soledad", 45, 3),
        ("cliente", "Maria", "Rodriguez", "maria@email.com", "3004443210", "Centro", "Barranquilla", 22, 2),
        ("cliente", "Luis", "Herrera", "luis@email.com", "3003332211", "El Prado", "Barranquilla", 30, 4),
        ("cliente", "Sofia", "Diaz", "sofia@email.com", "3002221100", "Villa Carolina", "Soledad", 26, 3),
        ("cliente", "Jorge", "Ramirez", "jorge@email.com", "3001119988", "Recreo", "Barranquilla", 50, 5),
        ("cliente", "Laura", "Torres", "laura@email.com", "3008887766", "Centro", "Barranquilla", 35, 2),
        ("empleado", "Diego", "Castro", "diego@freshmart.com", "3007776655", "El Prado", "Barranquilla", 40, 4),
        ("empleado", "Valentina", "Ruiz", "valentina@freshmart.com", "3006665544", "Alto Prado", "Barranquilla", 29, 5),
    ]
    
    ids = []
    for tipo, nombre, apellido, email, telefono, barrio, municipio, edad, estrato in personas:
        pid = uuid_from_time(time.time() + len(ids))
        ids.append(str(pid))
        session.execute(
            "INSERT INTO personas (id, nombre, apellido, tipo, email, telefono, barrio, municipio, edad, estrato) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (pid, nombre, apellido, tipo, email, telefono, barrio, municipio, edad, estrato)
        )
    
    cluster.shutdown()
    print(f"  -> {len(personas)} personas insertadas.")

def seed_mongo():
    print("\n[MongoDB] Insertando productos...")
    host = os.getenv('MONGO_HOST', '127.0.0.1')
    port = int(os.getenv('MONGO_PORT', 27017))
    db_name = os.getenv('MONGO_DB', 'freshmart')
    
    client = MongoClient(host=host, port=port)
    db = client[db_name]
    
    db.productos.delete_many({})
    
    productos = [
        {"id": str(uuid.uuid4()), "nombre": "Arroz Diana 1kg", "categoria": "Granos", "precio": 4500, "stock": 150, "tags": ["basico", "despensa", "carbohidrato"], "descripcion": "Arroz blanco de grano largo"},
        {"id": str(uuid.uuid4()), "nombre": "Aceite Girasol 1L", "categoria": "Aceites", "precio": 8900, "stock": 80, "tags": ["cocina", "grasas", "esencial"], "descripcion": "Aceite vegetal de girasol"},
        {"id": str(uuid.uuid4()), "nombre": "Leche Alqueria 1L", "categoria": "Lacteos", "precio": 3800, "stock": 200, "tags": ["lacteo", "calcio", "desayuno"], "descripcion": "Leche entera pasteurizada"},
        {"id": str(uuid.uuid4()), "nombre": "Pan Tajado Bimbo", "categoria": "Panaderia", "precio": 5200, "stock": 60, "tags": ["pan", "desayuno", "carbohidrato"], "descripcion": "Pan de molde blanco"},
        {"id": str(uuid.uuid4()), "nombre": "Huevos x30", "categoria": "Proteinas", "precio": 12500, "stock": 45, "tags": ["proteina", "desayuno", "esencial"], "descripcion": "Huevos de gallina clase A"},
        {"id": str(uuid.uuid4()), "nombre": "Pechuga Pollo 1kg", "categoria": "Carnes", "precio": 14800, "stock": 35, "tags": ["proteina", "carne", "saludable"], "descripcion": "Pechuga de pollo sin hueso"},
        {"id": str(uuid.uuid4()), "nombre": "Tomate x1kg", "categoria": "Verduras", "precio": 3200, "stock": 100, "tags": ["verdura", "ensalada", "fresco"], "descripcion": "Tomate rojo maduro"},
        {"id": str(uuid.uuid4()), "nombre": "Cebolla x1kg", "categoria": "Verduras", "precio": 2800, "stock": 90, "tags": ["verdura", "condimento", "basico"], "descripcion": "Cebolla cabezona blanca"},
        {"id": str(uuid.uuid4()), "nombre": "Papa x1kg", "categoria": "Verduras", "precio": 3500, "stock": 120, "tags": ["verdura", "carbohidrato", "basico"], "descripcion": "Papa pastusa"},
        {"id": str(uuid.uuid4()), "nombre": "Atun Van Camps 160g", "categoria": "Enlatados", "precio": 6200, "stock": 70, "tags": ["proteina", "enlatado", "omega3"], "descripcion": "Atun en aceite vegetal"},
        {"id": str(uuid.uuid4()), "nombre": "Cafe Juan Valdez 250g", "categoria": "Bebidas", "precio": 11500, "stock": 55, "tags": ["bebida", "cafe", "desayuno"], "descripcion": "Cafe molido tostado"},
        {"id": str(uuid.uuid4()), "nombre": "Azucar Refinar 1kg", "categoria": "Aseo", "precio": 3100, "stock": 110, "tags": ["endulzante", "basico", "despensa"], "descripcion": "Azucar blanca refinada"},
        {"id": str(uuid.uuid4()), "nombre": "Jabon Fab 125g", "categoria": "Aseo", "precio": 2200, "stock": 95, "tags": ["aseo", "limpieza", "hogar"], "descripcion": "Jabon de lavar ropa"},
        {"id": str(uuid.uuid4()), "nombre": "Papel Higienico x4", "categoria": "Aseo", "precio": 5800, "stock": 85, "tags": ["aseo", "hogar", "esencial"], "descripcion": "Papel higienico doble hoja"},
        {"id": str(uuid.uuid4()), "nombre": "Cerveza Aguila x6", "categoria": "Bebidas", "precio": 15900, "stock": 40, "tags": ["bebida", "alcohol", "festivo"], "descripcion": "Six pack de cerveza lager"},
    ]
    
    db.productos.insert_many(productos)
    client.close()
    print(f"  -> {len(productos)} productos insertados.")

def seed_mysql():
    print("\n[MySQL] Insertando facturas y detalles...")
    config = {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'root'),
        'database': os.getenv('MYSQL_DB', 'freshmart'),
    }
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM detalle_factura")
    cursor.execute("DELETE FROM factura")
    
    # Get product IDs from MongoDB
    client = MongoClient(host=os.getenv('MONGO_HOST', '127.0.0.1'), port=int(os.getenv('MONGO_PORT', 27017)))
    db = client[os.getenv('MONGO_DB', 'freshmart')]
    productos = list(db.productos.find())
    client.close()
    
    # Get persona IDs from Cassandra
    host = os.getenv('CASSANDRA_HOST', '127.0.0.1')
    keyspace = os.getenv('CASSANDRA_KEYSPACE', 'freshmart')
    cluster = Cluster([host], connection_class=AsyncioConnection)
    session = cluster.connect(keyspace)
    rows = session.execute("SELECT id, tipo FROM personas WHERE tipo = 'cliente' ALLOW FILTERING")
    clientes = [(str(r.id), r.tipo) for r in rows]
    cluster.shutdown()
    
    facturas_data = [
        (clientes[0][0], 3, [(0, 2, 4500), (2, 3, 3800), (4, 1, 12500)]),
        (clientes[1][0], 2, [(5, 1, 14800), (6, 2, 3200), (10, 1, 11500)]),
        (clientes[2][0], 4, [(0, 3, 4500), (1, 1, 8900), (8, 2, 3500), (11, 1, 3100)]),
        (clientes[3][0], 1, [(12, 3, 2200), (13, 2, 5800)]),
        (clientes[4][0], 2, [(5, 2, 14800), (9, 3, 6200), (14, 1, 15900)]),
        (clientes[5][0], 3, [(0, 1, 4500), (2, 2, 3800), (7, 1, 2800)]),
        (clientes[0][0], 1, [(10, 2, 11500), (4, 1, 12500)]),
        (clientes[1][0], 2, [(3, 1, 5200), (6, 3, 3200), (8, 1, 3500)]),
    ]
    
    for persona_id, idx, items in facturas_data:
        total = sum(cant * precio for _, cant, precio in items)
        cursor.execute(
            "INSERT INTO factura (persona_id, fecha, total) VALUES (%s, %s, %s)",
            (persona_id, datetime.now(), total)
        )
        factura_id = cursor.lastrowid
        
        for prod_idx, cant, precio in items:
            prod = productos[prod_idx]
            subtotal = cant * precio
            cursor.execute(
                "INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)",
                (factura_id, prod['id'], cant, precio, subtotal)
            )
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"  -> {len(facturas_data)} facturas con detalles insertadas.")

def seed_neo4j():
    print("\n[Neo4j] Creando grafo de relaciones...")
    uri = os.getenv('NEO4J_URI', 'bolt://127.0.0.1:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'neo4j')
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        
        # Get data from all sources
        host = os.getenv('CASSANDRA_HOST', '127.0.0.1')
        keyspace = os.getenv('CASSANDRA_KEYSPACE', 'freshmart')
        cluster = Cluster([host], connection_class=AsyncioConnection)
        session_cass = cluster.connect(keyspace)
        personas = list(session_cass.execute("SELECT * FROM personas"))
        cluster.shutdown()
        
        client = MongoClient(host=os.getenv('MONGO_HOST', '127.0.0.1'), port=int(os.getenv('MONGO_PORT', 27017)))
        db = client[os.getenv('MONGO_DB', 'freshmart')]
        productos = list(db.productos.find())
        client.close()
        
        config = {
            'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'root'),
            'database': os.getenv('MYSQL_DB', 'freshmart'),
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.persona_id, df.producto_id, df.cantidad
            FROM detalle_factura df
            JOIN factura f ON df.factura_id = f.id
        """)
        compras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Create Persona nodes
        for p in personas:
            rango_edad = _obtener_rango_edad(p.edad) if hasattr(p, 'edad') and p.edad else None
            session.run("""
                MERGE (per:Persona {id: $id})
                SET per.nombre = $nombre,
                    per.apellido = $apellido,
                    per.tipo = $tipo,
                    per.barrio = $barrio,
                    per.municipio = $municipio,
                    per.edad = $edad,
                    per.estrato = $estrato,
                    per.rango_edad = $rango_edad
            """, id=str(p.id), nombre=p.nombre, apellido=p.apellido, tipo=p.tipo,
                barrio=p.barrio, municipio=p.municipio, edad=p.edad, estrato=p.estrato, rango_edad=rango_edad)
        
        # Create Producto nodes
        for prod in productos:
            session.run("""
                MERGE (pr:Producto {id: $id})
                SET pr.nombre = $nombre,
                    pr.categoria = $categoria,
                    pr.precio = $precio
            """, id=prod['id'], nombre=prod['nombre'], categoria=prod['categoria'], precio=prod['precio'])
        
        # Create COMPRAS relationships
        for compra in compras:
            session.run("""
                MATCH (per:Persona {id: $persona_id})
                MATCH (pr:Producto {id: $producto_id})
                MERGE (per)-[c:COMPRO]->(pr)
                SET c.cantidad = coalesce(c.cantidad, 0) + $cantidad
            """, persona_id=compra['persona_id'], producto_id=compra['producto_id'], cantidad=compra['cantidad'])
        
        # Create VIVE_EN relationships (barrio)
        session.run("""
            MATCH (p:Persona)
            MERGE (b:Barrio {nombre: p.barrio})
            MERGE (p)-[:VIVE_EN]->(b)
        """)
        
        # Create UBICADO_EN relationships (municipio)
        session.run("""
            MATCH (p:Persona)
            MERGE (m:Municipio {nombre: p.municipio})
            MERGE (p)-[:UBICADO_EN]->(m)
        """)
        
        # Create MISMO_RANGO_EDAD relationships
        session.run("""
            MATCH (p1:Persona), (p2:Persona)
            WHERE p1.rango_edad = p2.rango_edad AND p1.id < p2.id
            MERGE (p1)-[:MISMO_RANGO_EDAD]-(p2)
        """)
        
        # Create MISMO_ESTRATO relationships
        session.run("""
            MATCH (p1:Persona), (p2:Persona)
            WHERE p1.estrato = p2.estrato AND p1.id < p2.id
            MERGE (p1)-[:MISMO_ESTRATO]-(p2)
        """)
        
        # Create COMPARTEN_CATEGORIA between products
        session.run("""
            MATCH (p1:Producto), (p2:Producto)
            WHERE p1.categoria = p2.categoria AND p1.id < p2.id
            MERGE (p1)-[:COMPARTEN_CATEGORIA]-(p2)
        """)
        
        print("  -> Grafo de relaciones creado correctamente.")
    
    driver.close()

if __name__ == "__main__":
    seed_all()
