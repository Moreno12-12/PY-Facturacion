from typing import Optional
from uuid import UUID

from src.domain.ports.persona_repository import PersonaRepository
from src.domain.entities.persona import Persona
from src.infrastructure.connections.cassandra_connection import CassandraConnection

class CassandraPersonaRepository(PersonaRepository):

    def __init__(self):
        conn = CassandraConnection()
        self.session = conn.connect("freshmart")

    def get_all(self) -> list[Persona]:
        rows = self.session.execute("SELECT * FROM personas")
        return [self._row_to_persona(r) for r in rows]

    def get_by_id(self, persona_id: UUID) -> Optional[Persona]:
        row = self.session.execute("SELECT * FROM personas WHERE id = %s", (persona_id,)).one()
        return self._row_to_persona(row) if row else None

    def get_clientes(self) -> list[Persona]:
        rows = self.session.execute("SELECT * FROM personas WHERE tipo = 'cliente' ALLOW FILTERING")
        return [self._row_to_persona(r) for r in rows]

    def create(self, persona: Persona) -> Persona:
        self.session.execute(
            """INSERT INTO personas (id, nombre, apellido, tipo, email, telefono, barrio, municipio, genero, estrato)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (persona.id, persona.nombre, persona.apellido, persona.tipo, persona.email,
             persona.telefono, persona.barrio, persona.municipio, persona.genero, persona.estrato)
        )
        return persona

    def update(self, persona: Persona) -> bool:
        self.session.execute(
            """UPDATE personas SET nombre = %s, apellido = %s, tipo = %s, email = %s,
               telefono = %s, barrio = %s, municipio = %s, genero = %s, estrato = %s
               WHERE id = %s""",
            (persona.nombre, persona.apellido, persona.tipo, persona.email,
             persona.telefono, persona.barrio, persona.municipio, persona.genero, persona.estrato, persona.id)
        )
        return True

    def delete(self, persona_id: UUID) -> bool:
        self.session.execute("DELETE FROM personas WHERE id = %s", (persona_id,))
        return True

    def count(self) -> int:
        rows = list(self.session.execute("SELECT COUNT(*) FROM personas"))
        return rows[0][0] if rows else 0

    def _row_to_persona(self, row) -> Persona:
        return Persona(
            id=row.id,
            nombre=row.nombre,
            apellido=row.apellido,
            tipo=row.tipo,
            email=row.email,
            telefono=row.telefono,
            barrio=row.barrio,
            municipio=row.municipio,
            genero=row.genero,
            estrato=row.estrato
        )
