from flask import Blueprint, render_template, request, jsonify
from extensions import db
from models import Compra, CompraDetalle, Producto
from models.proveedor import Proveedor

# Definimos el Blueprint
compras_bp = Blueprint('compras', __name__)

# Ruta para mostrar la página de compras
@compras_bp.route('/compras', methods=['GET'])
def mostrar_compras():
    return render_template('compras.html')

# Obtener todas las facturas de compras
@compras_bp.route('/api/compras', methods=['GET'])
def obtener_compras():
    compras = Compra.query.all()
    compras_list = []

    for compra in compras:
        detalles = CompraDetalle.query.filter_by(compra_id=compra.id).all()
        detalles_list = [{
            'producto_id': detalle.producto_id,
            'producto_nombre': detalle.producto_nombre,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.precio_unitario
        } for detalle in detalles]

        compras_list.append({
            'id': compra.id,
            'id_proveedor': compra.id_proveedor,
            'fecha_carga': compra.fecha_carga,
            'iva': compra.iva,
            'total': compra.total,
            'detalles': detalles_list
        })

    return jsonify(compras_list), 200

# Procesar una nueva factura de compra con detalles
@compras_bp.route('/api/procesar_compra', methods=['POST'])
def procesar_compra():
    data = request.get_json()

    # Validar los datos obligatorios de la compra
    if not data.get('id_proveedor'):
        return jsonify({"error": "ID del proveedor es obligatorio"}), 400

    # Obtener el IVA (opcional, por defecto 0)
    iva = data.get('iva', 0.0)

    # Verificar que se proporcionen los detalles
    if not data.get('detalles') or not isinstance(data['detalles'], list):
        return jsonify({"error": "Detalles de los productos no proporcionados o formato incorrecto"}), 400

    total_compra = 0

    # Procesar los detalles de la compra y calcular el total de los productos
    for detalle in data['detalles']:
        producto = None

        # Buscar el producto ya sea por id o por codigo1
        if 'producto_id' in detalle:
            producto = Producto.query.get(detalle['producto_id'])
        elif 'codigo1' in detalle:
            producto = Producto.query.filter_by(codigo1=detalle['codigo1']).first()

        if not producto:
            return jsonify({"error": "Producto no encontrado con el identificador proporcionado"}), 404

        # Convertir la cantidad a un número antes de multiplicar
        try:
            cantidad = int(detalle['cantidad'])  # Cambiar a float si se permiten decimales
        except ValueError:
            return jsonify({"error": "La cantidad debe ser un número válido"}), 400

        # Calcular el subtotal del producto basado en el costo del producto (desde la base de datos)
        subtotal_producto = cantidad * producto.costo
        total_compra += subtotal_producto

    # Al total de los productos le sumamos el IVA proporcionado
    total_final = total_compra + iva

    # Crear la nueva compra con el total final calculado
    nueva_compra = Compra(
        id_proveedor=data['id_proveedor'],
        iva=iva,
        total=total_final
    )

    db.session.add(nueva_compra)
    db.session.flush()  # Asegura que la compra tenga un ID generado antes de continuar

    # Ahora, crear los detalles de la compra con el ID de la compra generada
    for detalle in data['detalles']:
        nuevo_detalle = CompraDetalle(
            compra_id=nueva_compra.id,  # Utilizamos el ID generado para asignar el detalle a la compra
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            cantidad=cantidad,  # Usamos la cantidad convertida
            precio_unitario=producto.costo  # Usamos el costo del producto
        )

        # Actualizar el stock del producto
        producto.stock += cantidad

        # Guardamos el nuevo detalle
        db.session.add(nuevo_detalle)

    # Confirmar todos los cambios
    db.session.commit()

    return jsonify({"message": "Compra y detalles creados exitosamente", "compra_id": nueva_compra.id}), 201

@compras_bp.route('/api/proveedores', methods=['GET'])
def obtener_proveedores():
    proveedores = Proveedor.query.all()
    proveedores_list = [{
        'id': proveedor.id,
        'nombre': proveedor.nombre,
        'cuit': proveedor.cuit,
        'telefono': proveedor.telefono,
        'direccion': proveedor.direccion,
        'email': proveedor.email
    } for proveedor in proveedores]

    return jsonify(proveedores_list), 200