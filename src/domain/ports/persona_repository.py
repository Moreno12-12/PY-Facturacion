from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.domain.entities.persona import Persona

class PersonaRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Persona]:
        pass

    @abstractmethod
    def get_by_id(self, persona_id: UUID) -> Optional[Persona]:
        pass

    @abstractmethod
    def get_clientes(self) -> list[Persona]:
        pass

    @abstractmethod
    def create(self, persona: Persona) -> Persona:
        pass

    @abstractmethod
    def update(self, persona: Persona) -> bool:
        pass

    @abstractmethod
    def delete(self, persona_id: UUID) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
