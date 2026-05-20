from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.producto import Producto

class ProductoRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, producto_id: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def create(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def update(self, producto: Producto) -> bool:
        pass

    @abstractmethod
    def delete(self, producto_id: str) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
