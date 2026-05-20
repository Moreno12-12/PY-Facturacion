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

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})-[:COMPRO]->(prod:Producto)<-[:COMPRO]-(similar:Persona)
                WHERE similar.id <> $id
                AND NOT EXISTS {
                    MATCH (p)-[:COMPRO]->(prod2:Producto)
                    WHERE prod2.id = prod.id
                }
                WITH similar, prod, count(*) as score
                ORDER BY score DESC
                LIMIT 5
                RETURN prod.id as id, prod.nombre as nombre, prod.categoria as categoria,
                       prod.precio as precio, score
            """, id=cliente_id)

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

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})-[:VIVE_EN|:MISMO_ESTRATO|:COMPARTEN_GENERO]-(similar:Persona)
                WHERE similar.id <> $id AND similar.tipo = 'cliente'
                WITH similar, count(*) as conexion
                ORDER BY conexion DESC
                LIMIT 6
                RETURN similar.nombre as nombre, similar.apellido as apellido,
                       similar.barrio as barrio, similar.estrato as estrato, conexion
            """, id=cliente_id)

            return [ClienteSimilar(
                nombre=r['nombre'],
                apellido=r['apellido'],
                barrio=r['barrio'],
                estrato=r['estrato'],
                conexion=r['conexion']
            ) for r in result]

    def obtener_productos_comprados(self, cliente_id: str) -> list[dict]:
        if self.driver is None:
            return []

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})-[c:COMPRO]->(prod:Producto)
                RETURN prod.nombre as nombre, c.cantidad as cantidad
                ORDER BY c.cantidad DESC
            """, id=cliente_id)

            return [dict(r) for r in result]

    def obtener_perfil_cliente(self, cliente_id: str) -> Optional[dict]:
        if self.driver is None:
            return None

        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Persona {id: $id})
                RETURN p
            """, id=cliente_id)

            record = result.single()
            if record:
                p = record['p']
                return {
                    "id": p['id'],
                    "nombre": p['nombre'],
                    "apellido": p['apellido'],
                    "barrio": p['barrio'],
                    "municipio": p['municipio'],
                    "genero": p['genero'],
                    "estrato": p['estrato']
                }
            return None

    def _obtener_razones(self, session, cliente_id: str, producto_id: str) -> list:
        razones = []

        barrio_result = session.run("""
            MATCH (p:Persona {id: $id})-[:VIVE_EN]->(b:Barrio)<-[:VIVE_EN]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id, prod_id=producto_id)
        barrio_rec = barrio_result.single()
        if barrio_rec and barrio_rec['count'] > 0:
            razones.append(f"Comprado por {barrio_rec['count']} persona(s) de tu mismo barrio")

        estrato_result = session.run("""
            MATCH (p:Persona {id: $id})-[:MISMO_ESTRATO]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id, prod_id=producto_id)
        estrato_rec = estrato_result.single()
        if estrato_rec and estrato_rec['count'] > 0:
            razones.append(f"Popular en personas de estrato similar ({estrato_rec['count']})")

        genero_result = session.run("""
            MATCH (p:Persona {id: $id})-[:COMPARTEN_GENERO]-(similar:Persona)-[:COMPRO]->(prod:Producto {id: $prod_id})
            RETURN count(similar) as count
        """, id=cliente_id, prod_id=producto_id)
        genero_rec = genero_result.single()
        if genero_rec and genero_rec['count'] > 0:
            razones.append(f"Comprado por personas del mismo genero ({genero_rec['count']})")

        categoria_result = session.run("""
            MATCH (p:Persona {id: $id})-[:COMPRO]->(otro:Producto)-[:COMPARTEN_CATEGORIA]-(prod:Producto {id: $prod_id})
            RETURN count(otro) as count
        """, id=cliente_id, prod_id=producto_id)
        categoria_rec = categoria_result.single()
        if categoria_rec and categoria_rec['count'] > 0:
            razones.append(f"Relacionado con productos que has comprado ({categoria_rec['count']})")

        if not razones:
            razones.append("Recomendado basado en patrones de compra similares")

        return razones
