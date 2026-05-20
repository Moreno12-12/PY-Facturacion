from typing import Optional
from uuid import UUID, uuid4
import time

from src.domain.ports.persona_repository import PersonaRepository
from src.domain.entities.persona import Persona
from src.application.dto.persona_dto import CrearPersonaDTO, ActualizarPersonaDTO
from cassandra.util import uuid_from_time

class PersonaService:

    def __init__(self, repository: PersonaRepository):
        self.repository = repository

    def obtener_todas(self) -> list[Persona]:
        return self.repository.get_all()

    def obtener_por_id(self, persona_id: str) -> Optional[Persona]:
        return self.repository.get_by_id(UUID(persona_id))

    def obtener_clientes(self) -> list[Persona]:
        return self.repository.get_clientes()

    def crear(self, dto: CrearPersonaDTO) -> Persona:
        persona_id = uuid_from_time(time.time())
        persona = dto.to_persona(persona_id)
        return self.repository.create(persona)

    def actualizar(self, dto: ActualizarPersonaDTO) -> bool:
        persona = dto.to_persona()
        return self.repository.update(persona)

    def eliminar(self, persona_id: str) -> bool:
        return self.repository.delete(UUID(persona_id))

    def contar(self) -> int:
        return self.repository.count()
