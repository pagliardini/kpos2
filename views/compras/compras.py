from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.compra import Compra, CompraDetalle
from models.proveedor import Proveedor
from extensions import db
from datetime import datetime
import json

compras_bp = Blueprint('compras', __name__)


# Ruta para mostrar los productos
@compras_bp.route('/compras')
def compras():
    proveedores = Proveedor.query.all()

    return render_template('compras.html', proveedores=proveedores)


@compras_bp.route('/buscar_producto', methods=['POST'])
def buscar_producto():
    # Obtén el código del producto desde el formulario o la solicitud AJAX
    codigo = request.json.get('codigo')  # Enviaremos los datos como JSON

    if not codigo:
        return jsonify({"error": "Código no proporcionado"}), 400

    # Busca el producto en la base de datos
    producto = Producto.query.filter_by(codigo1=codigo).first()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Si encuentra el producto, retorna los datos como JSON
    producto_data = {
        "id": producto.id,
        "nombre": producto.nombre,
        "costo": producto.costo,
        "precio": producto.precio,
        "codigo1": producto.codigo1,
        "stock": producto.stock,
        "marca_id": producto.marca_id,
        "rubro_id": producto.rubro_id,
        "tipo_id": producto.tipo_id
    }

    return jsonify(producto_data)


@compras_bp.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    data = request.json
    print("Datos recibidos:", data)  # Muestra todos los datos recibidos

    # Obtener datos de la compra
    id_proveedor = data.get('id_proveedor')
    iva = data.get('iva', 0)
    total = data.get('total', 0)
    detalles = data.get('detalles', [])
    fecha_carga = data.get('fecha_compra')  # Obtener la fecha del JSON

    # Agregar una verificación para la fecha
    if fecha_carga == '':
        print("No se proporcionó fecha. Usando fecha y hora actuales.")
        fecha_carga = datetime.now()  # Usa la fecha y hora actuales
    else:
        print("Fecha cargada:", fecha_carga)  # Mostrar la fecha recibida

        # Convertir la cadena de fecha a un objeto datetime
        fecha_carga = datetime.strptime(fecha_carga, '%Y-%m-%d')  # Asegúrate de que el formato sea correcto

    # Crear una nueva compra
    nueva_compra = Compra(id_proveedor=id_proveedor, iva=iva, total=total, fecha_carga=fecha_carga)

    db.session.add(nueva_compra)

    # Guardar cambios para obtener el ID de la compra
    db.session.commit()

    # Agregar detalles de la compra y actualizar stock
    for detalle in detalles:
        # Buscar el producto por su código (codigo1) en lugar de usar el id directamente
        producto = Producto.query.filter_by(codigo1=detalle['producto_id']).first()

        if producto:
            nuevo_detalle = CompraDetalle(
                compra_id=nueva_compra.id,
                producto_id=producto.id,  # Aquí usamos el ID del producto real, no el código
                producto_nombre=producto.nombre,
                cantidad=detalle['cantidad'],
                precio_unitario=detalle['precio_unitario']
            )

            db.session.add(nuevo_detalle)

            # Actualizar el stock del producto
            producto.stock += detalle['cantidad']

    # Confirmar todos los cambios en la base de datos
    try:
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()  # Revertir cambios si hay error
        return jsonify({"error": str(e)}), 500
