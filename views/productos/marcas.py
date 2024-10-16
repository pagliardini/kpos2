from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.producto import Marca


marcas_bp = Blueprint('marcas', __name__)


@marcas_bp.route('/marcas', methods=['GET'])
def listar_marcas():
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)


@marcas_bp.route('/marcas/agregar', methods=['POST'])
def agregar_marca():
    nombre = request.form['nombre']
    nueva_marca = Marca(nombre=nombre)
    db.session.add(nueva_marca)
    db.session.commit()
    flash('Marca agregada exitosamente')

    return redirect(url_for('marcas.listar_marcas'))


@marcas_bp.route('/marcas/editar/<int:id>', methods=['GET', 'POST'])
def editar_marca(id):
    marca = Marca.query.get_or_404(id)
    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        flash('Marca actualizada exitosamente')
        return redirect(url_for('marcas.listar_marcas'))
    return render_template('editar_marca.html', marca=marca)


@marcas_bp.route('/marcas/eliminar/<int:id>', methods=['POST'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)
    db.session.delete(marca)
    db.session.commit()
    flash('Marca eliminada exitosamente')
    return redirect(url_for('marcas.listar_marcas'))
