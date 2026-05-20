from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.application.services.factura_service import FacturaService
from src.application.services.persona_service import PersonaService
from src.application.dto.factura_dto import CrearFacturaDTO
from src.application.dto.producto_dto import ItemFacturaDTO

factura_bp = Blueprint('facturas', __name__, url_prefix='/facturas')

def create_factura_controller(factura_service: FacturaService, persona_service: PersonaService):

    @factura_bp.route('/')
    def index():
        facturas = factura_service.obtener_todas()
        total_general = factura_service.obtener_total_general()

        facturas_data = []
        for f in facturas:
            persona = persona_service.obtener_por_id(f.persona_id)
            facturas_data.append({
                'id': f.id,
                'persona_id': f.persona_id,
                'cliente_nombre': persona.nombre if persona else '',
                'cliente_apellido': persona.apellido if persona else '',
                'fecha': f.fecha,
                'total': f.total,
                'estado': f.estado
            })

        return render_template('facturas.html', facturas=facturas_data, total_general=total_general)

    @factura_bp.route('/<int:factura_id>')
    def detalle(factura_id):
        detalle_dto = factura_service.obtener_detalle(factura_id)
        if not detalle_dto:
            flash('Factura no encontrada.', 'danger')
            return redirect(url_for('facturas.index'))

        persona = persona_service.obtener_por_id(detalle_dto.persona_id)
        if persona:
            detalle_dto.cliente_nombre = persona.nombre
            detalle_dto.cliente_apellido = persona.apellido

        return render_template('factura_detalle.html', factura=detalle_dto)

    @factura_bp.route('/nueva', methods=['GET', 'POST'])
    def nueva():
        clientes = persona_service.obtener_clientes()

        if request.method == 'POST':
            producto_ids = request.form.getlist('producto_id')
            cantidades = request.form.getlist('cantidad')

            items = []
            for i in range(len(producto_ids)):
                if producto_ids[i]:
                    items.append(ItemFacturaDTO(
                        producto_id=producto_ids[i],
                        cantidad=int(cantidades[i])
                    ))

            dto = CrearFacturaDTO(
                persona_id=request.form['persona_id'],
                items=items
            )

            factura_id = factura_service.crear(dto)
            flash('Factura generada exitosamente.', 'success')
            return redirect(url_for('facturas.detalle', factura_id=factura_id))

        from src.infrastructure.connections.mongo_connection import MongoConnection
        mongo_conn = MongoConnection()
        db = mongo_conn.connect()
        productos = list(db.productos.find().sort("nombre", 1))

        return render_template('nueva_factura.html', clientes=clientes, productos=productos)

    @factura_bp.route('/anular/<int:factura_id>')
    def anular(factura_id):
        factura_service.anular(factura_id)
        flash('Factura anulada.', 'warning')
        return redirect(url_for('facturas.index'))

    return factura_bp
