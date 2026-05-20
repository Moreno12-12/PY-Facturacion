from typing import Optional

from src.domain.ports.producto_repository import ProductoRepository
from src.domain.entities.producto import Producto
from src.infrastructure.connections.mongo_connection import MongoConnection

class MongoProductoRepository(ProductoRepository):

    def __init__(self):
        conn = MongoConnection()
        self.db = conn.connect()
        self.collection = self.db.productos

    def get_all(self) -> list[Producto]:
        docs = list(self.collection.find().sort("nombre", 1))
        return [self._doc_to_producto(d) for d in docs]

    def get_by_id(self, producto_id: str) -> Optional[Producto]:
        doc = self.collection.find_one({"id": producto_id})
        return self._doc_to_producto(doc) if doc else None

    def create(self, producto: Producto) -> Producto:
        doc = self._producto_to_doc(producto)
        self.collection.insert_one(doc)
        return producto

    def update(self, producto: Producto) -> bool:
        self.collection.update_one(
            {"id": producto.id},
            {"$set": self._producto_to_doc(producto)}
        )
        return True

    def delete(self, producto_id: str) -> bool:
        self.collection.delete_one({"id": producto_id})
        return True

    def count(self) -> int:
        return self.collection.count_documents({})

    def _doc_to_producto(self, doc: dict) -> Producto:
        return Producto(
            id=doc["id"],
            nombre=doc["nombre"],
            categoria=doc["categoria"],
            precio=float(doc["precio"]),
            stock=int(doc.get("stock", 0)),
            descripcion=doc.get("descripcion"),
            tags=doc.get("tags", [])
        )

    def _producto_to_doc(self, producto: Producto) -> dict:
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio": producto.precio,
            "stock": producto.stock,
            "descripcion": producto.descripcion,
            "tags": producto.tags
        }
