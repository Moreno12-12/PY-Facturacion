from dataclasses import dataclass
from typing import Optional

@dataclass
class DetalleFactura:
    id: Optional[int] = None
    factura_id: Optional[int] = None
    producto_id: str = ""
    cantidad: int = 1
    precio_unitario: float = 0.0
    subtotal: float = 0.0
    producto_nombre: str = "Producto desconocido"

    def calcular_subtotal(self) -> float:
        self.subtotal = self.cantidad * self.precio_unitario
        return self.subtotal

    @property
    def subtotal_formateado(self) -> str:
        return f"$ {self.subtotal:,.0f}"

    @property
    def precio_unitario_formateado(self) -> str:
        return f"$ {self.precio_unitario:,.0f}"
