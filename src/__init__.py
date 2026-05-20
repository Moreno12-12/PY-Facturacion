from src.domain import Persona, Producto, Factura, DetalleFactura, Recomendacion, ClienteSimilar
from src.domain import PersonaRepository, ProductoRepository, FacturaRepository, RecomendacionRepository
from src.application import PersonaService, ProductoService, FacturaService, RecomendacionService
from src.infrastructure import CassandraPersonaRepository, MongoProductoRepository, MySQLFacturaRepository, Neo4jRecomendacionRepository
