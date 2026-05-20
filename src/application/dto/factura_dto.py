from dataclasses import dataclass
from typing import Optional
from src.application.dto.producto_dto import ItemFacturaDTO

@dataclass
class CrearFacturaDTO:
    persona_id: str
    items: list[ItemFacturaDTO]

@dataclass
class FacturaDetalleViewDTO:
    factura_id: int
    persona_id: str
    cliente_nombre: str
    cliente_apellido: str
    fecha: str
    total: float
    estado: str
    detalles: list[dict]

    @property
    def total_formateado(self) -> str:
        return f"$ {self.total:,.0f}"
