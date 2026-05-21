from typing import Optional
from datetime import datetime

from src.domain.ports.factura_repository import FacturaRepository
from src.domain.ports.producto_repository import ProductoRepository
from src.domain.entities.factura import Factura
from src.domain.entities.detalle_factura import DetalleFactura
from src.application.dto.factura_dto import CrearFacturaDTO, FacturaDetalleViewDTO

class FacturaService:

    def __init__(self, factura_repo: FacturaRepository, producto_repo: ProductoRepository, neo4j_repo=None):
        self.factura_repo = factura_repo
        self.producto_repo = producto_repo
        self.neo4j_repo = neo4j_repo

    def obtener_todas(self) -> list[Factura]:
        return self.factura_repo.get_all()

    def obtener_detalle(self, factura_id: int) -> Optional[FacturaDetalleViewDTO]:
        factura = self.factura_repo.get_by_id(factura_id)
        if not factura:
            return None

        detalles = self.factura_repo.get_detalles(factura_id)
        detalles_data = []

        for d in detalles:
            prod = self.producto_repo.get_by_id(d.producto_id)
            if prod:
                d.producto_nombre = prod.nombre
            detalles_data.append({
                "producto_nombre": d.producto_nombre,
                "cantidad": d.cantidad,
                "precio_unitario": d.precio_unitario,
                "subtotal": d.subtotal
            })

        return FacturaDetalleViewDTO(
            factura_id=factura.id,
            persona_id=factura.persona_id,
            cliente_nombre="",
            cliente_apellido="",
            fecha=factura.fecha.strftime("%Y-%m-%d %H:%M:%S") if factura.fecha else "",
            total=factura.total,
            estado=factura.estado,
            detalles=detalles_data
        )

    def crear(self, dto: CrearFacturaDTO) -> int:
        factura = Factura(
            persona_id=dto.persona_id,
            fecha=datetime.now(),
            estado="activa"
        )

        detalles = []
        total = 0.0

        for item in dto.items:
            prod = self.producto_repo.get_by_id(item.producto_id)
            if prod:
                detalle = DetalleFactura(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=prod.precio
                )
                detalle.calcular_subtotal()
                detalles.append(detalle)
                total += detalle.subtotal

        factura.total = total
        factura_id = self.factura_repo.create(factura, detalles)
        if self.neo4j_repo:
            productos_info = {}
            for item in dto.items:
                prod = self.producto_repo.get_by_id(item.producto_id)
                if prod:
                    productos_info[item.producto_id] = prod
            self.neo4j_repo.sincronizar_compras(factura.persona_id, detalles, productos_info)
        return factura_id

    def anular(self, factura_id: int) -> bool:
        return self.factura_repo.anular(factura_id)

    def eliminar(self, factura_id: int) -> bool:
        return self.factura_repo.eliminar(factura_id)

    def obtener_total_general(self) -> float:
        return self.factura_repo.get_total_general()

    def contar(self) -> int:
        return self.factura_repo.count()
