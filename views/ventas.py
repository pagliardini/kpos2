from flask import Blueprint, render_template, request, redirect, url_for
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
@ventas_bp.route('/procesar_venta', methods=['POST'])
def procesar_venta():
    # Obtener productos seleccionados del formulario
    ids_productos = request.form.getlist('productos')

    if ids_productos:
        total_venta = 0
        for id_producto in ids_productos:
            producto = Producto.query.get(id_producto)
            if producto:
                total_venta += producto.precio

        # Crear la nueva factura
        nueva_factura = Factura(total=total_venta)
        db.session.add(nueva_factura)
        db.session.commit()

    return redirect(url_for('ventas.ventas'))
