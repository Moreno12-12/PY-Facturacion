from flask import Blueprint, render_template, request

from src.application.services.recomendacion_service import RecomendacionService
from src.application.services.persona_service import PersonaService

recomendacion_bp = Blueprint('recomendaciones', __name__, url_prefix='/recomendaciones')

def create_recomendacion_controller(recomendacion_service: RecomendacionService, persona_service: PersonaService):

    @recomendacion_bp.route('/')
    def index():
        clientes = persona_service.obtener_clientes()
        cliente_id = request.args.get('cliente_id')
        cliente = None
        recomendaciones = []
        productos_comprados = []
        clientes_similares = []

        if cliente_id:
            cliente = recomendacion_service.obtener_perfil_cliente(cliente_id)
            recomendaciones = recomendacion_service.obtener_recomendaciones(cliente_id)
            productos_comprados = recomendacion_service.obtener_productos_comprados(cliente_id)
            clientes_similares = recomendacion_service.obtener_clientes_similares(cliente_id)

        return render_template(
            'recomendaciones.html',
            clientes=clientes,
            cliente_id=cliente_id,
            cliente=cliente,
            recomendaciones=recomendaciones,
            productos_comprados=productos_comprados,
            clientes_similares=clientes_similares
        )

    return recomendacion_bp
