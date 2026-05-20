from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template

from src.infrastructure.connections.cassandra_connection import CassandraConnection
from src.infrastructure.connections.mongo_connection import MongoConnection
from src.infrastructure.connections.mysql_connection import MySQLConnection
from src.infrastructure.connections.neo4j_connection import Neo4jConnection

from src.infrastructure.adapters import (
    CassandraPersonaRepository,
    MongoProductoRepository,
    MySQLFacturaRepository,
    Neo4jRecomendacionRepository
)

from src.application.services import (
    PersonaService,
    ProductoService,
    FacturaService,
    RecomendacionService
)

from web.controllers.persona_controller import create_persona_controller
from web.controllers.producto_controller import create_producto_controller
from web.controllers.factura_controller import create_factura_controller
from web.controllers.recomendacion_controller import create_recomendacion_controller


def create_app() -> Flask:
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'web', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'web', 'static'))
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecreto123')

    # Initialize connections
    CassandraConnection().connect("freshmart")
    MongoConnection().connect()
    MySQLConnection().connect()
    Neo4jConnection().connect()

    # Initialize repositories (adapters)
    persona_repo = CassandraPersonaRepository()
    producto_repo = MongoProductoRepository()
    factura_repo = MySQLFacturaRepository()
    recomendacion_repo = Neo4jRecomendacionRepository()

    # Initialize services (application layer)
    persona_service = PersonaService(persona_repo)
    producto_service = ProductoService(producto_repo)
    factura_service = FacturaService(factura_repo, producto_repo)
    recomendacion_service = RecomendacionService(recomendacion_repo)

    # Register controllers (web layer)
    app.register_blueprint(create_persona_controller(persona_service))
    app.register_blueprint(create_producto_controller(producto_service))
    app.register_blueprint(create_factura_controller(factura_service, persona_service))
    app.register_blueprint(create_recomendacion_controller(recomendacion_service, persona_service))

    @app.route("/")
    def index():
        return render_template("index.html",
                               total_personas=persona_service.contar(),
                               total_productos=producto_service.contar(),
                               total_facturas=factura_service.contar())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
