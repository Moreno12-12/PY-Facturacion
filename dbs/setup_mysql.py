import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

import mysql.connector

def setup():
    config = {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'root'),
    }
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    db_name = os.getenv('MYSQL_DB', 'freshmart')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factura (
            id INT AUTO_INCREMENT PRIMARY KEY,
            persona_id VARCHAR(36) NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10, 2) DEFAULT 0.00,
            estado ENUM('activa', 'anulada') DEFAULT 'activa'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_factura (
            id INT AUTO_INCREMENT PRIMARY KEY,
            factura_id INT NOT NULL,
            producto_id VARCHAR(36) NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("MySQL: Base de datos, tablas 'factura' y 'detalle_factura' creadas correctamente.")

if __name__ == "__main__":
    setup()
