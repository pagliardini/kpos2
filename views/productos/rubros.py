from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto import Rubro
from extensions import db


rubros_bp = Blueprint('rubros', __name__)

@rubros_bp.route('/rubros', methods=['GET'])
def listar_rubros():
    rubros = Rubro.query.all()
    return render_template('rubros.html', rubros=rubros)


@rubros_bp.route('/rubros/agregar', methods=['POST'])
def agregar_rubro():
    nombre = request.form['nombre']
    nuevo_rubro = Rubro(nombre=nombre)
    db.session.add(nuevo_rubro)
    db.session.commit()
    flash('Rubro agregado exitosamente')

    return redirect(url_for('productos.listar_rubros'))


@rubros_bp.route('/rubros/editar/<int:id>', methods=['GET', 'POST'])
def editar_rubro(id):
    rubro = Rubro.query.get_or_404(id)
    if request.method == 'POST':
        rubro.nombre = request.form['nombre']
        db.session.commit()
        flash('Rubro actualizado exitosamente')
        return redirect(url_for('productos.listar_rubros'))
    return render_template('editar_rubro.html', rubro=rubro)


@rubros_bp.route('/rubros/eliminar/<int:id>', methods=['POST'])
def eliminar_rubro(id):
    rubro = Rubro.query.get_or_404(id)
    db.session.delete(rubro)
    db.session.commit()
    flash('Rubro eliminado exitosamente')
    return redirect(url_for('productos.listar_rubros'))