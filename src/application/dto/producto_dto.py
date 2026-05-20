from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CrearProductoDTO:
    nombre: str
    categoria: str
    precio: float
    stock: int = 0
    descripcion: Optional[str] = None
    tags: list = field(default_factory=list)

    def to_producto(self, producto_id: str):
        from src.domain.entities.producto import Producto
        return Producto(
            id=producto_id,
            nombre=self.nombre,
            categoria=self.categoria,
            precio=self.precio,
            stock=self.stock,
            descripcion=self.descripcion,
            tags=self.tags
        )

@dataclass
class ActualizarProductoDTO:
    producto_id: str
    nombre: str
    categoria: str
    precio: float
    stock: int = 0
    descripcion: Optional[str] = None
    tags: list = field(default_factory=list)

    def to_producto(self):
        from src.domain.entities.producto import Producto
        return Producto(
            id=self.producto_id,
            nombre=self.nombre,
            categoria=self.categoria,
            precio=self.precio,
            stock=self.stock,
            descripcion=self.descripcion,
            tags=self.tags
        )

@dataclass
class ItemFacturaDTO:
    producto_id: str
    cantidad: int
