from typing import Optional
import uuid

from src.domain.ports.producto_repository import ProductoRepository
from src.domain.entities.producto import Producto
from src.application.dto.producto_dto import CrearProductoDTO, ActualizarProductoDTO

class ProductoService:

    def __init__(self, repository: ProductoRepository):
        self.repository = repository

    def obtener_todos(self) -> list[Producto]:
        return self.repository.get_all()

    def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        return self.repository.get_by_id(producto_id)

    def crear(self, dto: CrearProductoDTO) -> Producto:
        producto_id = str(uuid.uuid4())
        producto = dto.to_producto(producto_id)
        return self.repository.create(producto)

    def actualizar(self, dto: ActualizarProductoDTO) -> bool:
        producto = dto.to_producto()
        return self.repository.update(producto)

    def eliminar(self, producto_id: str) -> bool:
        return self.repository.delete(producto_id)

    def contar(self) -> int:
        return self.repository.count()
