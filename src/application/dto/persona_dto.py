from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class CrearPersonaDTO:
    nombre: str
    apellido: str
    tipo: str
    email: str
    telefono: Optional[str] = None
    barrio: Optional[str] = None
    municipio: Optional[str] = None
    edad: Optional[str] = None
    estrato: Optional[int] = None

    def to_persona(self, persona_id: UUID):
        from src.domain.entities.persona import Persona
        return Persona(
            id=persona_id,
            nombre=self.nombre,
            apellido=self.apellido,
            tipo=self.tipo,
            email=self.email,
            telefono=self.telefono,
            barrio=self.barrio,
            municipio=self.municipio,
            edad=self.edad,
            estrato=self.estrato
        )

@dataclass
class ActualizarPersonaDTO:
    persona_id: UUID
    nombre: str
    apellido: str
    tipo: str
    email: str
    telefono: Optional[str] = None
    barrio: Optional[str] = None
    municipio: Optional[str] = None
    edad: Optional[str] = None
    estrato: Optional[int] = None

    def to_persona(self):
        from src.domain.entities.persona import Persona
        return Persona(
            id=self.persona_id,
            nombre=self.nombre,
            apellido=self.apellido,
            tipo=self.tipo,
            email=self.email,
            telefono=self.telefono,
            barrio=self.barrio,
            municipio=self.municipio,
            edad=self.edad,
            estrato=self.estrato
        )
