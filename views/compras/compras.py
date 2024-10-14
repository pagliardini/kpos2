from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.compra import Compra, CompraDetalle
from models.proveedor import Proveedor
from extensions import db

compras_bp = Blueprint('compras', __name__)

# Ruta para mostrar las compras
@compras_bp.route('/compras')
def compras():
    proveedores = Proveedor.query.all()  # Asegúrate de importar el modelo Proveedor
    return render_template('compras.html', proveedores=proveedores)

# Ruta para procesar la compra
@compras_bp.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    data = request.get_json()
    productos = data.get('productos', [])
    total_compra = 0

    if productos:
        detalles_compra = []

        for producto_data in productos:
            id_producto = producto_data.get('id')
            cantidad = producto_data.get('cantidad', 1)

            # Buscar el producto por ID
            producto = Producto.query.get(id_producto)
            if producto:
                # Aumentar el stock del producto
                producto.stock += cantidad
                total_compra += float(producto.precio) * int(cantidad)

                # Crear el detalle de la compra
                detalle = CompraDetalle(
                    producto_id=producto.id,
                    producto_nombre=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                detalles_compra.append(detalle)

                # Guardar los cambios del stock en la base de datos
                db.session.commit()
            else:
                print(f"Producto con ID {id_producto} no encontrado.")

        # Crear la nueva compra y agregar los detalles
        nueva_compra = Compra(total=total_compra, iva=21.0)  # Agregar IVA si es necesario
        db.session.add(nueva_compra)
        db.session.commit()  # Necesario para generar el ID de la compra

        for detalle in detalles_compra:
            detalle.compra_id = nueva_compra.id
            db.session.add(detalle)

        db.session.commit()  # Guardar los detalles en la base de datos

    return redirect(url_for('compras.compras'))

# Ruta para buscar productos
@compras_bp.route('/buscar_producto')
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

@compras_bp.route('/buscar_producto_descripcion')
def buscar_producto_descripcion():
    descripcion = request.args.get('descripcion')
    productos = Producto.query.filter(Producto.nombre.ilike(f'%{descripcion}%')).all()
    return jsonify([{
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio
    } for producto in productos])
