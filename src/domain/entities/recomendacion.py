from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Recomendacion:
    producto_id: str
    nombre: str
    categoria: str
    precio: float
    score: int = 0
    razones: list = field(default_factory=list)

    @property
    def precio_formateado(self) -> str:
        return f"$ {self.precio:,.0f}"

@dataclass
class ClienteSimilar:
    nombre: str
    apellido: str
    barrio: str
    estrato: int
    conexion: int = 0

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
