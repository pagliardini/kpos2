from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.factura import Factura, FacturaDetalle
from extensions import db
import json

ventas_bp = Blueprint('ventas', __name__)


# Ruta para mostrar los productos
@ventas_bp.route('/ventas')
def ventas():
    productos = Producto.query.all()  # Obtener todos los productos
    return render_template('ventas.html', productos=productos)


# Ruta para procesar la venta
@ventas_bp.route('/procesar_venta', methods=['POST'])
def procesar_venta():
    # Obtener JSON enviado en el cuerpo de la petición
    data = request.get_json()

    productos = data.get('productos', [])
    total_venta = 0

    if productos:
        detalles_factura = []

        # Calcular el total y preparar los detalles de la venta
        for producto_data in productos:
            id_producto = producto_data.get('id')
            cantidad = producto_data.get('cantidad', 1)

            # Buscar el producto por ID
            producto = Producto.query.get(id_producto)
            if producto and producto.precio:
                # Calcular el total de la venta
                total_venta += float(producto.precio) * int(cantidad)

                # Crear el detalle de la factura con el nombre del producto
                detalle = FacturaDetalle(
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                detalles_factura.append(detalle)

                # Descontar el stock del producto, permitiendo que sea negativo
                producto.stock -= cantidad

            else:
                print(f"Producto con ID {id_producto} no encontrado o sin precio")

        print(f"Total de la venta calculado: {total_venta}")

        # Crear la nueva factura y agregar los detalles
        if total_venta > 0:
            nueva_factura = Factura(total=total_venta)
            db.session.add(nueva_factura)
            db.session.commit()  # Necesario para generar el ID de la factura

            # Asignar los detalles de la factura a la factura recién creada
            for detalle in detalles_factura:
                detalle.factura_id = nueva_factura.id
                db.session.add(detalle)

            db.session.commit()  # Guardar los detalles en la base de datos

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

