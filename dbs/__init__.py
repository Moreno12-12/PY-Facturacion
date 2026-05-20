import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dbs import setup_cassandra, setup_mongo, setup_mysql, setup_neo4j, seed_data

def main():
    print("=" * 60)
    print("FreshMart - Configuracion completa de bases de datos")
    print("=" * 60)
    
    print("\n[1/5] Configurando Cassandra...")
    setup_cassandra.setup()
    
    print("\n[2/5] Configurando MongoDB...")
    setup_mongo.setup()
    
    print("\n[3/5] Configurando MySQL...")
    setup_mysql.setup()
    
    print("\n[4/5] Configurando Neo4j...")
    setup_neo4j.setup()
    
    print("\n[5/5] Cargando datos de prueba...")
    seed_data.seed_all()
    
    print("\n" + "=" * 60)
    print("Proyecto FreshMart listo para usar!")
    print("=" * 60)

if __name__ == "__main__":
    main()
