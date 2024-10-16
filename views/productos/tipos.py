from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.producto import Tipo


tipos_bp = Blueprint('tipos', __name__)


@tipos_bp.route('/tipos', methods=['GET'])
def listar_tipos():
    tipos = Tipo.query.all()
    return render_template('tipos.html', tipos=tipos)


@tipos_bp.route('/tipos/agregar', methods=['POST'])
def agregar_tipo():
    nombre = request.form['nombre']
    nuevo_tipo = Tipo(nombre=nombre)
    db.session.add(nuevo_tipo)
    db.session.commit()
    flash('Tipo agregado exitosamente')
    return redirect(url_for('tipos.listar_tipos'))


@tipos_bp.route('/tipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_tipo(id):
    tipo = Tipo.query.get_or_404(id)
    if request.method == 'POST':
        tipo.nombre = request.form['nombre']
        db.session.commit()
        flash('Tipo actualizado exitosamente')
        return redirect(url_for('tipos.listar_tipos'))
    return render_template('editar_tipo.html', tipo=tipo)


@tipos_bp.route('/tipos/eliminar/<int:id>', methods=['POST'])
def eliminar_tipo(id):
    tipo = Tipo.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    flash('Tipo eliminado exitosamente')
    return redirect(url_for('tipos.listar_tipos'))