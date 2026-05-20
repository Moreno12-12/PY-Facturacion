from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class Persona:
    id: UUID
    nombre: str
    apellido: str
    tipo: str
    email: str
    telefono: Optional[str] = None
    barrio: Optional[str] = None
    municipio: Optional[str] = None
    genero: Optional[str] = None
    estrato: Optional[int] = None

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    @property
    def es_cliente(self) -> bool:
        return self.tipo == "cliente"

    @property
    def es_empleado(self) -> bool:
        return self.tipo == "empleado"
