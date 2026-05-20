from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.application.services.producto_service import ProductoService
from src.application.dto.producto_dto import CrearProductoDTO, ActualizarProductoDTO

producto_bp = Blueprint('productos', __name__, url_prefix='/productos')

def create_producto_controller(service: ProductoService):

    @producto_bp.route('/')
    def index():
        productos = service.obtener_todos()
        return render_template('productos.html', productos=productos)

    @producto_bp.route('/nuevo', methods=['GET', 'POST'])
    def nuevo():
        if request.method == 'POST':
            tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
            dto = CrearProductoDTO(
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                stock=int(request.form.get('stock', 0)),
                descripcion=request.form.get('descripcion'),
                tags=tags
            )
            service.crear(dto)
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('productos.index'))
        return render_template('producto_form.html', titulo='Nuevo Producto', producto=None)

    @producto_bp.route('/editar/<producto_id>', methods=['GET', 'POST'])
    def editar(producto_id):
        if request.method == 'POST':
            tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
            dto = ActualizarProductoDTO(
                producto_id=producto_id,
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                stock=int(request.form.get('stock', 0)),
                descripcion=request.form.get('descripcion'),
                tags=tags
            )
            service.actualizar(dto)
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('productos.index'))

        producto = service.obtener_por_id(producto_id)
        return render_template('producto_form.html', titulo='Editar Producto', producto=producto)

    @producto_bp.route('/eliminar/<producto_id>')
    def eliminar(producto_id):
        service.eliminar(producto_id)
        flash('Producto eliminado.', 'info')
        return redirect(url_for('productos.index'))

    return producto_bp
