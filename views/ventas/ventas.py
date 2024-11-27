from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.producto import Producto
from models.factura import Factura, FacturaDetalle, FormaCobro
from extensions import db
from bs4 import BeautifulSoup
import requests

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
    forma_cobro_id = data.get('forma_cobro_id')  # Obtener la forma de cobro del JSON
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

                # Actualizar stock
                if cantidad < 0:
                    producto.stock += abs(cantidad)
                else:
                    producto.stock -= cantidad

                db.session.commit()
            else:
                print(f"Producto con ID {id_producto} no encontrado o sin precio")

        # Si no se proporciona una forma de cobro, buscar la predeterminada
        if not forma_cobro_id:
            forma_cobro_default = FormaCobro.query.filter_by(es_default=True).first()
            forma_cobro_id = forma_cobro_default.id if forma_cobro_default else None

        # Crear la nueva factura con la forma de cobro
        nueva_factura = Factura(total=total_venta, forma_cobro_id=forma_cobro_id)
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

@ventas_bp.route('/ventas/formascobro', methods=['GET'])
def formas_cobro():
    formas_cobro = FormaCobro.query.all()
    formas_cobrojson = [{'id': forma.id, 'denominacion': forma.denominacion, 'recargo': forma.recargo} for forma in formas_cobro]
    return jsonify(formas_cobrojson)

@ventas_bp.route('/ventas/pricely/<ean>', methods=['GET'])
def proxy_pricely(ean):
    try:
        # Hacer la solicitud a Pricely
        url = f"https://pricely.ar/product/{ean}"
        response = requests.get(url)
        response.raise_for_status()  # Verifica que el estado HTTP sea 200

        # Analizar el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el nombre del producto
        nombre_producto = soup.select_one(
            "body > main > div > div.max-w-5xl.w-full.bg-white.p-8.md\\:p-4.shadow-xl.mb-8 > div.flex.items-center.md\\:flex-row.gap-4.w-full.flex-col.md\\:p-4 > div.flex.flex-col.justify-center > h1"
        )
        nombre_producto = nombre_producto.text.strip() if nombre_producto else "Nombre no encontrado"

        # Extraer el precio promedio
        precio_promedio = soup.select_one(
            "body > main > div > div.max-w-5xl.w-full.bg-white.p-8.md\\:p-4.shadow-xl.mb-8 > div.md\\:p-4.mt-4 > div > div > div.flex.flex-col.md\\:flex-row.items-center.justify-between.gap-4.mt-8 > div > h3"
        )
        precio_promedio = precio_promedio.text.strip() if precio_promedio else "Precio no encontrado"

        # Retornar la información como JSON
        return jsonify({
            "nombre": nombre_producto,
            "precio": precio_promedio
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al conectarse con Pricely", "details": str(e)}), 500
    except AttributeError:
        return jsonify({"error": "No se pudo extraer información del producto."}), 500