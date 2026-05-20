from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Producto:
    id: str
    nombre: str
    categoria: str
    precio: float
    stock: int = 0
    descripcion: Optional[str] = None
    tags: list = field(default_factory=list)

    @property
    def precio_formateado(self) -> str:
        return f"$ {self.precio:,.0f}"

    @property
    def disponible(self) -> bool:
        return self.stock > 0

    def agregar_tags(self, tags_str: str) -> list:
        self.tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        return self.tags
