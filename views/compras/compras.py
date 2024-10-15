from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.compra import Compra, CompraDetalle
from models.proveedor import Proveedor
from extensions import db
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