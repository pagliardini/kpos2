from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Producto  # Asegúrate de que tienes un modelo Producto definido
from extensions import db  # Importa tu instancia de base de datos

productos_bp = Blueprint('productos', __name__)

# Ruta para mostrar todos los productos
@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()  # Obtener todos los productos de la base de datos
    return render_template('productos.html', productos=productos)

# Ruta para agregar un nuevo producto
@productos_bp.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    codigo = request.form['codigo']
    # Crear un nuevo producto y agregarlo a la base de datos
    nuevo_producto = Producto(nombre=nombre, precio=precio, codigo1=codigo)
    db.session.add(nuevo_producto)
    db.session.commit()
    flash('Producto agregado exitosamente')
    return redirect(url_for('productos.listar_productos'))

# Ruta para actualizar un producto
@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        db.session.commit()
        flash('Producto actualizado exitosamente')
        return redirect(url_for('productos.listar_productos'))
    return render_template('editar_producto.html', producto=producto)

# Ruta para eliminar un producto
@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('productos.listar_productos'))
