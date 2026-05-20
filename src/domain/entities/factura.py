from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Factura:
    id: Optional[int] = None
    persona_id: str = ""
    fecha: Optional[datetime] = None
    total: float = 0.0
    estado: str = "activa"

    @property
    def esta_activa(self) -> bool:
        return self.estado == "activa"

    @property
    def esta_anulada(self) -> bool:
        return self.estado == "anulada"

    def anular(self) -> None:
        self.estado = "anulada"

    @property
    def total_formateado(self) -> str:
        return f"$ {self.total:,.0f}"
