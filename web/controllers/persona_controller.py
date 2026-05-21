from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.application.services.persona_service import PersonaService
from src.application.dto.persona_dto import CrearPersonaDTO, ActualizarPersonaDTO

persona_bp = Blueprint('personas', __name__, url_prefix='/personas')

def create_persona_controller(service: PersonaService):

    @persona_bp.route('/')
    def index():
        personas = service.obtener_todas()
        return render_template('personas.html', personas=personas)

    @persona_bp.route('/nueva', methods=['GET', 'POST'])
    def nueva():
        if request.method == 'POST':
            dto = CrearPersonaDTO(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                tipo=request.form['tipo'],
                email=request.form['email'],
                telefono=request.form.get('telefono'),
                barrio=request.form.get('barrio'),
                municipio=request.form.get('municipio'),
                edad=int(request.form.get('edad', 18)),
                estrato=int(request.form.get('estrato', 1))
            )
            service.crear(dto)
            flash('Persona creada exitosamente.', 'success')
            return redirect(url_for('personas.index'))
        return render_template('persona_form.html', titulo='Nueva Persona', persona=None)

    @persona_bp.route('/editar/<persona_id>', methods=['GET', 'POST'])
    def editar(persona_id):
        if request.method == 'POST':
            dto = ActualizarPersonaDTO(
                persona_id=__import__('uuid').UUID(persona_id),
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                tipo=request.form['tipo'],
                email=request.form['email'],
                telefono=request.form.get('telefono'),
                barrio=request.form.get('barrio'),
                municipio=request.form.get('municipio'),
                edad=int(request.form.get('edad', 18)),
                estrato=int(request.form.get('estrato', 1))
            )
            service.actualizar(dto)
            flash('Persona actualizada exitosamente.', 'success')
            return redirect(url_for('personas.index'))

        persona = service.obtener_por_id(persona_id)
        return render_template('persona_form.html', titulo='Editar Persona', persona=persona)

    @persona_bp.route('/eliminar/<persona_id>')
    def eliminar(persona_id):
        service.eliminar(persona_id)
        flash('Persona eliminada.', 'info')
        return redirect(url_for('personas.index'))

    return persona_bp
