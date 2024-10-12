from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.producto import Producto, Rubro, Marca, Tipo
from extensions import db

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    marcas = Marca.query.all()
    rubros = Rubro.query.all()
    tipos = Tipo.query.all()

    if request.accept_mimetypes.best == 'application/json':
        return jsonify({
            'productos': [producto.to_dict() for producto in productos],
            'marcas': [marca.to_dict() for marca in marcas],
            'rubros': [rubro.to_dict() for rubro in rubros],
            'tipos': [tipo.to_dict() for tipo in tipos]
        })

    return render_template('productos.html', productos=productos, marcas=marcas, rubros=rubros, tipos=tipos)


@productos_bp.route('/api/productos', methods=['GET'])
def listar_productos_api():
    productos = Producto.query.all()

    # Retornar la lista de productos en formato JSON
    return jsonify({
        'productos': [producto.to_dict() for producto in productos]
    }), 200  # 200 OK


@productos_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    codigo = request.form.get('codigo')

    # Validar si ya existe el producto con el código proporcionado (opcional)
    producto_existente = Producto.query.filter_by(codigo1=codigo).first()
    if producto_existente:
        flash('El producto ya existe.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    # Si no existe, procede a agregar el producto
    nuevo_producto = Producto(
        nombre=request.form.get('nombre'),
        precio=request.form.get('precio'),
        costo=request.form.get('costo'),
        codigo1=codigo,
        marca_id=request.form.get('marca_id'),
        rubro_id=request.form.get('rubro_id'),
        tipo_id=request.form.get('tipo_id')
    )
    db.session.add(nuevo_producto)
    db.session.commit()

    flash('Producto agregado exitosamente!', 'success')
    return redirect(url_for('productos.listar_productos'))


@productos_bp.route('/api/agregar_producto', methods=['POST'])
def agregar_producto_api():
    if request.is_json:
        data = request.get_json()

        # Validar si ya existe el producto con el código proporcionado
        producto_existente = Producto.query.filter_by(codigo1=data['codigo']).first()
        if producto_existente:
            return {'message': 'El producto ya existe.'}, 400

        # Si no existe, procede a agregar el producto
        nuevo_producto = Producto(
            nombre=data['nombre'],
            precio=data['precio'],
            codigo1=data['codigo'],
            marca_id=data['marca_id'],
            rubro_id=data['rubro_id'],
            tipo_id=data['tipo_id']
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        return {'message': 'Producto agregado exitosamente!'}, 201
    else:
        return {'message': 'La solicitud no es JSON.'}, 400


@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.marca_id = request.form['marca_id']
        producto.rubro_id = request.form['rubro_id']
        producto.tipo_id = request.form['tipo_id']
        db.session.commit()
        flash('Producto actualizado exitosamente')
        return redirect(url_for('productos.listar_productos'))
    return render_template('editar_producto.html', producto=producto)


@productos_bp.route('/api/productos/editar/<int:id>', methods=['PUT'])
def editar_producto_api(id):
    producto = Producto.query.get_or_404(id)

    if request.is_json:
        data = request.get_json()
        producto.nombre = data.get('nombre', producto.nombre)  # Si el campo no está presente, no se cambia
        producto.precio = data.get('precio', producto.precio)
        producto.marca_id = data.get('marca_id', producto.marca_id)
        producto.rubro_id = data.get('rubro_id', producto.rubro_id)
        producto.tipo_id = data.get('tipo_id', producto.tipo_id)

        db.session.commit()

        return {'message': 'Producto actualizado exitosamente'}, 200
    else:
        return {'message': 'La solicitud no es JSON'}, 400


@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('productos.listar_productos'))


@productos_bp.route('/api/productos/eliminar/<int:id>', methods=['DELETE'])
def eliminar_producto_api(id):
    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    return {'message': 'Producto eliminado exitosamente'}, 200
