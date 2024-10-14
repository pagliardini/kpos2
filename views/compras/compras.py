from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.compra import Compra, CompraDetalle
from models.proveedor import Proveedor
from extensions import db

compras_bp = Blueprint('compras', __name__)

# Ruta para mostrar el formulario de compras
@compras_bp.route('/compras')
def compras():
    proveedores = Proveedor.query.all()
    return render_template('compras.html', proveedores=proveedores)

# Ruta para procesar la compra
@compras_bp.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    data = request.get_json()
    proveedor_id = data.get('proveedor')
    productos = data.get('productos', [])
    iva = data.get('iva', 0)
    total = data.get('total', 0)

    if productos:
        detalles_compra = []

        # Crear la compra principal
        nueva_compra = Compra(id_proveedor=proveedor_id, iva=iva, total=total)
        db.session.add(nueva_compra)
        db.session.commit()  # Necesario para obtener el ID de la compra

        # Procesar cada producto
        for producto_data in productos:
            producto_id = producto_data.get('id')
            cantidad = producto_data.get('cantidad', 1)
            precio_unitario = producto_data.get('precio_unitario')

            producto = Producto.query.get(producto_id)
            if producto:
                # Crear el detalle de la compra
                detalle = CompraDetalle(
                    compra_id=nueva_compra.id,
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
                detalles_compra.append(detalle)

                # Actualizar el stock del producto
                producto.stock += cantidad
                db.session.commit()

        # Guardar los detalles de la compra en la base de datos
        for detalle in detalles_compra:
            db.session.add(detalle)
        db.session.commit()

    return redirect(url_for('compras.compras'))

# Ruta para buscar producto por código
@compras_bp.route('/buscar_producto', methods=['GET'])
def buscar_producto():
    codigo = request.args.get('codigo')  # Obtener el código enviado
    producto = Producto.query.filter_by(codigo1=codigo).first()  # Buscar el producto por codigo1

    if producto:
        # Devolver toda la información del producto en formato JSON
        return jsonify({
            'id': producto.id,
            'nombre': producto.nombre,
            'costo': producto.costo,
            'precio': producto.precio,
            'codigo1': producto.codigo1,
            'stock': producto.stock
        })
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404
