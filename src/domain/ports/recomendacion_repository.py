from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.recomendacion import Recomendacion, ClienteSimilar

class RecomendacionRepository(ABC):

    @abstractmethod
    def obtener_recomendaciones(self, cliente_id: str) -> list[Recomendacion]:
        pass

    @abstractmethod
    def obtener_clientes_similares(self, cliente_id: str) -> list[ClienteSimilar]:
        pass

    @abstractmethod
    def obtener_productos_comprados(self, cliente_id: str) -> list[dict]:
        pass

    @abstractmethod
    def obtener_perfil_cliente(self, cliente_id: str) -> Optional[dict]:
        pass
