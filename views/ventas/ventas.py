from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.factura import Factura, FacturaDetalle
from extensions import db

ventas_bp = Blueprint('ventas', __name__)

# Ruta para mostrar la página de ventas
@ventas_bp.route('/ventas')
def ventas():
    return render_template('ventas.html')

# Ruta para procesar la venta
@ventas_bp.route('/ventas/procesar', methods=['POST'])
def procesar_venta():
    data = request.get_json()
    productos = data.get('productos', [])
    total_venta = 0

    if productos:
        detalles_factura = []

        for producto_data in productos:
            id_producto = producto_data.get('id')
            cantidad = producto_data.get('cantidad', 1)
            producto = Producto.query.get(id_producto)

            if producto and producto.precio:
                total_venta += float(producto.precio) * int(cantidad)
                detalle = FacturaDetalle(
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                detalles_factura.append(detalle)

                if cantidad < 0:
                    producto.stock += abs(cantidad)
                else:
                    producto.stock -= cantidad

                db.session.commit()
            else:
                print(f"Producto con ID {id_producto} no encontrado o sin precio")

        nueva_factura = Factura(total=total_venta)
        db.session.add(nueva_factura)
        db.session.commit()

        for detalle in detalles_factura:
            detalle.factura_id = nueva_factura.id
            db.session.add(detalle)

        db.session.commit()

    return redirect(url_for('ventas.ventas'))

# Ruta para buscar producto por código
@ventas_bp.route('/ventas/buscar/codigo')
def buscar_producto():
    codigo = request.args.get('codigo')
    producto = Producto.query.filter_by(codigo1=codigo).first()
    if producto:
        return jsonify({
            'id': producto.id,
            'codigo': producto.codigo1,
            'nombre': producto.nombre,
            'precio': producto.precio
        })
    return jsonify(None), 404

# Ruta para buscar producto por descripción
@ventas_bp.route('/ventas/buscar/descripcion')
def buscar_producto_descripcion():
    descripcion = request.args.get('descripcion')
    productos = Producto.query.filter(Producto.nombre.ilike(f'%{descripcion}%')).all()
    return jsonify([{
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio
    } for producto in productos])

# Ruta para buscar producto por ID
@ventas_bp.route('/ventas/buscar/id')
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
