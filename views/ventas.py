from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.factura import Factura
from extensions import db

ventas_bp = Blueprint('ventas', __name__)


# Ruta para mostrar los productos
@ventas_bp.route('/ventas')
def ventas():
    productos = Producto.query.all()  # Obtener todos los productos
    return render_template('ventas.html', productos=productos)


# Ruta para procesar la venta
# Ruta para procesar la venta
@ventas_bp.route('/procesar_venta', methods=['POST'])
def procesar_venta():
    # Obtener IDs de productos seleccionados desde el formulario
    ids_productos = request.form.getlist('productos')  # Aquí usas IDs en lugar de códigos de barras

    if ids_productos:
        total_venta = 0
        for id_producto in ids_productos:
            producto = Producto.query.get(id_producto)  # Seguimos utilizando el ID (int) para buscar el producto
            if producto:
                total_venta += producto.precio

        # Crear la nueva factura
        nueva_factura = Factura(total=total_venta)
        db.session.add(nueva_factura)
        db.session.commit()

    return redirect(url_for('ventas.ventas'))
@ventas_bp.route('/buscar_producto')
def buscar_producto():
    codigo = request.args.get('codigo')
    producto = Producto.query.filter_by(codigo1=codigo).first()
    if producto:
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio
        })
    return jsonify(None), 404

@ventas_bp.route('/buscar_producto_descripcion')
def buscar_producto_descripcion():
    descripcion = request.args.get('descripcion')
    productos = Producto.query.filter(Producto.nombre.ilike(f'%{descripcion}%')).all()
    return jsonify([{
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio
    } for producto in productos])
@ventas_bp.route('/buscar_producto_por_id')
def buscar_producto_por_id():
    id_producto = request.args.get('id')
    producto = Producto.query.get(id_producto)
    if producto:
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio
        })
    return jsonify(None), 404

