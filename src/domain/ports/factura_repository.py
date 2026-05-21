from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.factura import Factura
from src.domain.entities.detalle_factura import DetalleFactura

class FacturaRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Factura]:
        pass

    @abstractmethod
    def get_by_id(self, factura_id: int) -> Optional[Factura]:
        pass

    @abstractmethod
    def get_detalles(self, factura_id: int) -> list[DetalleFactura]:
        pass

    @abstractmethod
    def create(self, factura: Factura, detalles: list[DetalleFactura]) -> int:
        pass

    @abstractmethod
    def anular(self, factura_id: int) -> bool:
        pass

    @abstractmethod
    def eliminar(self, factura_id: int) -> bool:
        pass

    @abstractmethod
    def get_total_general(self) -> float:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
