from typing import Optional

from src.domain.ports.recomendacion_repository import RecomendacionRepository
from src.domain.entities.recomendacion import Recomendacion, ClienteSimilar

class RecomendacionService:

    def __init__(self, repository: RecomendacionRepository):
        self.repository = repository

    def obtener_recomendaciones(self, cliente_id: str) -> list[Recomendacion]:
        return self.repository.obtener_recomendaciones(cliente_id)

    def obtener_clientes_similares(self, cliente_id: str) -> list[ClienteSimilar]:
        return self.repository.obtener_clientes_similares(cliente_id)

    def obtener_productos_comprados(self, cliente_id: str) -> list[dict]:
        return self.repository.obtener_productos_comprados(cliente_id)

    def obtener_perfil_cliente(self, cliente_id: str) -> Optional[dict]:
        return self.repository.obtener_perfil_cliente(cliente_id)
