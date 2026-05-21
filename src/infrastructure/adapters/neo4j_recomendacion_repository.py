from typing import Optional

from src.domain.ports.recomendacion_repository import RecomendacionRepository
from src.domain.entities.recomendacion import Recomendacion, ClienteSimilar
from src.infrastructure.connections.neo4j_connection import Neo4jConnection

class Neo4jRecomendacionRepository(RecomendacionRepository):

    def __init__(self):
        conn = Neo4jConnection()
        self.driver = conn.connect()

    def obtener_recomendaciones(self, cliente_id: str) -> list[Recomendacion]:
        if self.driver is None:
            return []

        cliente_id_str = str(cliente_id)

        with self.driver.session() as session:
            result = session.run("""
                MATCH (similar:Persona)-[:COMPRO]->(prod:Producto)
                WHERE similar.id <> $id
                AND NOT EXISTS {
                    MATCH (p:Persona {id: $id})-[:COMPRO]->(prod:Producto)
                }
                AND EXISTS {
                    MATCH (p:Persona {id: $id})-[:VIVE_EN|:MISMO_ESTRATO|:MISMO_RANGO_EDAD]-(similar)
                }
                WITH similar, prod, count(*) as score
                ORDER BY score DESC
                LIMIT 5
                RETURN prod.id as id, prod.nombre as nombre, prod.categoria as categoria,
                       prod.precio as precio, score
            """, id=cliente_id_str)

            recs = [dict(r) for r in result]
            recomendaciones = []

            for rec in recs:
                razones = self._obtener_razones(session, cliente_id, rec['id'])
                recomendaciones.append(Recomendacion(
                    producto_id=rec['id'],
                    nombre=rec['nombre'],
                    categoria=rec['categoria'],
                    precio=float(rec['precio']),
                    score=rec['score'],
                    razones=razones
                ))

            return recomendaciones

    def obtener_clientes_similares(self, cliente_id: str) -> list[ClienteSimilar]:
        if self.driver is None:
            return []

        cliente_id_str = str(cliente_id)

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})-[:VIVE_EN|:MISMO_ESTRATO|:MISMO_RANGO_EDAD]-(similar:Persona)
                WHERE similar.id <> $id AND similar.tipo = 'cliente'
                WITH similar, count(*) as conexion
                ORDER BY conexion DESC
                LIMIT 6
                RETURN similar.nombre as nombre, similar.apellido as apellido,
                       similar.barrio as barrio, similar.estrato as estrato, similar.edad as edad, conexion
            """, id=cliente_id_str)

            return [ClienteSimilar(
                nombre=r['nombre'],
                apellido=r['apellido'],
                barrio=r['barrio'],
                estrato=r['estrato'],
                edad=r.get('edad'),
                conexion=r['conexion']
            ) for r in result]

    def obtener_productos_comprados(self, cliente_id: str) -> list[dict]:
        if self.driver is None:
            return []

        cliente_id_str = str(cliente_id)

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})-[c:COMPRO]->(prod:Producto)
                RETURN prod.nombre as nombre, c.cantidad as cantidad
                ORDER BY c.cantidad DESC
            """, id=cliente_id_str)

            return [dict(r) for r in result]

    def obtener_perfil_cliente(self, cliente_id: str) -> Optional[dict]:
        if self.driver is None:
            return None

        cliente_id_str = str(cliente_id)

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})
                RETURN p
            """, id=cliente_id_str)

            record = result.single()
            if record:
                p = record['p']
                return {
                    "id": p['id'],
                    "nombre": p['nombre'],
                    "apellido": p['apellido'],
                    "barrio": p['barrio'],
                    "municipio": p['municipio'],
                    "edad": p.get('edad'),
                    "rango_edad": p.get('rango_edad'),
                    "estrato": p['estrato']
                }
            return None

    def _obtener_razones(self, session, cliente_id: str, producto_id: str) -> list:
        razones = []
        cliente_id_str = str(cliente_id)

        barrio_result = session.run("""
            MATCH (p:Persona {id: $id})-[:VIVE_EN]->(b:Barrio)<-[:VIVE_EN]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id_str, prod_id=producto_id)
        barrio_rec = barrio_result.single()
        if barrio_rec and barrio_rec['count'] > 0:
            razones.append(f"Comprado por {barrio_rec['count']} persona(s) de tu mismo barrio")

        estrato_result = session.run("""
            MATCH (p:Persona {id: $id})-[:MISMO_ESTRATO]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id_str, prod_id=producto_id)
        estrato_rec = estrato_result.single()
        if estrato_rec and estrato_rec['count'] > 0:
            razones.append(f"Popular en personas de estrato similar ({estrato_rec['count']})")

        edad_result = session.run("""
            MATCH (p:Persona {id: $id})-[:MISMO_RANGO_EDAD]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id_str, prod_id=producto_id)
        edad_rec = edad_result.single()
        if edad_rec and edad_rec['count'] > 0:
            razones.append(f"Popular en personas de tu misma edad ({edad_rec['count']})")

        categoria_result = session.run("""
            MATCH (p:Persona {id: $id})-[:COMPRO]->(otro:Producto)-[:COMPARTEN_CATEGORIA]-(prod:Producto {id: $prod_id})
            RETURN count(otro) as count
        """, id=cliente_id_str, prod_id=producto_id)
        categoria_rec = categoria_result.single()
        if categoria_rec and categoria_rec['count'] > 0:
            razones.append(f"Relacionado con productos que has comprado ({categoria_rec['count']})")

        if not razones:
            razones.append("Recomendado basado en patrones de compra similares")

        return razones

    def sincronizar_persona(self, persona) -> None:
        if self.driver is None:
            return

        rango_edad = self._obtener_rango_edad(persona.edad) if persona.edad else None

        with self.driver.session() as session:
            session.run("""
                MERGE (per:Persona {id: $id})
                SET per.nombre = $nombre,
                    per.apellido = $apellido,
                    per.tipo = $tipo,
                    per.barrio = $barrio,
                    per.municipio = $municipio,
                    per.edad = $edad,
                    per.estrato = $estrato,
                    per.rango_edad = $rango_edad
            """, id=str(persona.id), nombre=persona.nombre, apellido=persona.apellido,
                tipo=persona.tipo, barrio=persona.barrio, municipio=persona.municipio,
                edad=persona.edad, estrato=persona.estrato, rango_edad=rango_edad)

            session.run("""
                MATCH (p:Persona {id: $id})
                MERGE (b:Barrio {nombre: p.barrio})
                MERGE (p)-[:VIVE_EN]->(b)
            """, id=str(persona.id))

            session.run("""
                MATCH (p:Persona {id: $id})
                MERGE (m:Municipio {nombre: p.municipio})
                MERGE (p)-[:UBICADO_EN]->(m)
            """, id=str(persona.id))

            session.run("""
                MATCH (p1:Persona {id: $id}), (p2:Persona)
                WHERE p1.rango_edad = p2.rango_edad AND p1.id <> p2.id
                MERGE (p1)-[:MISMO_RANGO_EDAD]-(p2)
            """, id=str(persona.id))

            session.run("""
                MATCH (p1:Persona {id: $id}), (p2:Persona)
                WHERE p1.estrato = p2.estrato AND p1.id <> p2.id
                MERGE (p1)-[:MISMO_ESTRATO]-(p2)
            """, id=str(persona.id))

    def _obtener_rango_edad(self, edad: int) -> str:
        if edad is None:
            return "desconocido"
        if edad < 18:
            return "menor_18"
        elif edad < 25:
            return "18_24"
        elif edad < 35:
            return "25_34"
        elif edad < 45:
            return "35_44"
        elif edad < 55:
            return "45_54"
        elif edad < 65:
            return "55_64"
        else:
            return "65_plus"

    def eliminar_persona_neo4j(self, persona_id: str) -> None:
        if self.driver is None:
            return

        with self.driver.session() as session:
            session.run("""
                MATCH (p:Persona {id: $id})
                DETACH DELETE p
            """, id=str(persona_id))

    def sincronizar_compras(self, persona_id: str, detalles: list, productos_info: dict = None) -> None:
        if self.driver is None:
            return

        persona_id_str = str(persona_id)

        with self.driver.session() as session:
            for d in detalles:
                prod_info = productos_info.get(d.producto_id) if productos_info else None
                if prod_info:
                    session.run("""
                        MATCH (per:Persona {id: $persona_id})
                        MERGE (prod:Producto {id: $producto_id})
                        SET prod.nombre = $nombre, prod.categoria = $categoria, prod.precio = $precio
                        MERGE (per)-[c:COMPRO]->(prod)
                        SET c.cantidad = coalesce(c.cantidad, 0) + $cantidad
                    """, persona_id=persona_id_str, producto_id=d.producto_id,
                        nombre=prod_info.nombre, categoria=prod_info.categoria,
                        precio=prod_info.precio, cantidad=d.cantidad)
                else:
                    session.run("""
                        MATCH (per:Persona {id: $persona_id})
                        MERGE (prod:Producto {id: $producto_id})
                        MERGE (per)-[c:COMPRO]->(prod)
                        SET c.cantidad = coalesce(c.cantidad, 0) + $cantidad
                    """, persona_id=persona_id_str, producto_id=d.producto_id, cantidad=d.cantidad)
