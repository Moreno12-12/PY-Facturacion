from typing import Optional
from datetime import datetime

from src.domain.ports.factura_repository import FacturaRepository
from src.domain.entities.factura import Factura
from src.domain.entities.detalle_factura import DetalleFactura
from src.infrastructure.connections.mysql_connection import MySQLConnection

class MySQLFacturaRepository(FacturaRepository):

    def __init__(self):
        conn = MySQLConnection()
        self.connection = conn.connect()

    def get_all(self) -> list[Factura]:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM factura ORDER BY fecha DESC")
        facturas = [self._row_to_factura(r) for r in cursor.fetchall()]
        cursor.close()
        return facturas

    def get_by_id(self, factura_id: int) -> Optional[Factura]:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM factura WHERE id = %s", (factura_id,))
        row = cursor.fetchone()
        cursor.close()
        return self._row_to_factura(row) if row else None

    def get_detalles(self, factura_id: int) -> list[DetalleFactura]:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detalle_factura WHERE factura_id = %s", (factura_id,))
        detalles = [self._row_to_detalle(r) for r in cursor.fetchall()]
        cursor.close()
        return detalles

    def create(self, factura: Factura, detalles: list[DetalleFactura]) -> int:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO factura (persona_id, fecha, total, estado) VALUES (%s, %s, %s, %s)",
            (factura.persona_id, factura.fecha, factura.total, factura.estado)
        )
        factura_id = cursor.lastrowid

        for d in detalles:
            cursor.execute(
                "INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)",
                (factura_id, d.producto_id, d.cantidad, d.precio_unitario, d.subtotal)
            )

        self.connection.commit()
        cursor.close()
        return factura_id

    def anular(self, factura_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("UPDATE factura SET estado = 'anulada' WHERE id = %s", (factura_id,))
        self.connection.commit()
        cursor.close()
        return True

    def eliminar(self, factura_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM detalle_factura WHERE factura_id = %s", (factura_id,))
        cursor.execute("DELETE FROM factura WHERE id = %s", (factura_id,))
        self.connection.commit()
        cursor.close()
        return True

    def get_total_general(self) -> float:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COALESCE(SUM(total), 0) as total FROM factura WHERE estado = 'activa'")
        result = cursor.fetchone()
        cursor.close()
        return float(result['total']) if result else 0

    def count(self) -> int:
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM factura")
        result = cursor.fetchone()
        cursor.close()
        return result['cnt'] if result else 0

    def _row_to_factura(self, row: dict) -> Factura:
        return Factura(
            id=row['id'],
            persona_id=row['persona_id'],
            fecha=row['fecha'],
            total=float(row['total']),
            estado=row['estado']
        )

    def _row_to_detalle(self, row: dict) -> DetalleFactura:
        return DetalleFactura(
            id=row['id'],
            factura_id=row['factura_id'],
            producto_id=row['producto_id'],
            cantidad=row['cantidad'],
            precio_unitario=float(row['precio_unitario']),
            subtotal=float(row['subtotal'])
        )
