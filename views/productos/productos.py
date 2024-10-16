from xml.etree.ElementPath import prepare_descendant

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.producto import Producto, Rubro, Marca, Tipo
from extensions import db
import pandas as pd

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    limit = request.args.get('limit', 50, type=int)  # Limitar a 50 por defecto
    offset = request.args.get('offset', 0, type=int)

    productos = Producto.query.limit(limit).offset(offset).all()
    marcas = Marca.query.all()
    rubros = Rubro.query.all()
    tipos = Tipo.query.all()

    if request.accept_mimetypes.best == 'application/json':
        return jsonify({
            'productos': [producto.to_dict() for producto in productos],
            'marcas': [marca.to_dict() for marca in marcas],
            'rubros': [rubro.to_dict() for rubro in rubros],
            'tipos': [tipo.to_dict() for tipo in tipos]
        }), 200
    else:
        return render_template('productos.html', productos=productos, marcas=marcas, rubros=rubros, tipos=tipos)


@productos_bp.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    # Inicializar variables desde request.form o request.get_json() según el tipo de solicitud
    if request.is_json:
        data = request.get_json()
        codigo = data.get('codigo')
        nombre = data.get('nombre')
        precio = data.get('precio')
        costo = data.get('costo')
        marca_id = data.get('marca_id')
        rubro_id = data.get('rubro_id')
        tipo_id = data.get('tipo_id')
    else:
        codigo = request.form.get('codigo')
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        costo = request.form.get('costo')
        marca_id = request.form.get('marca_id')
        rubro_id = request.form.get('rubro_id')
        tipo_id = request.form.get('tipo_id')

    # Validar si ya existe el producto con el código proporcionado
    producto_existente = Producto.query.filter_by(codigo1=codigo).first()
    if producto_existente:
        if request.is_json:
            return {'message': 'El producto ya existe.'}, 400
        else:
            flash('El producto ya existe.', 'danger')
            return redirect(url_for('productos.listar_productos'))

    # Crear el nuevo producto
    nuevo_producto = Producto(
        nombre=nombre,
        precio=precio,
        costo=costo,
        codigo1=codigo,
        marca_id=marca_id,
        rubro_id=rubro_id,
        tipo_id=tipo_id
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    if request.is_json:
        return {'message': 'Producto agregado exitosamente!'}, 201
    else:
        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('productos.listar_productos'))



@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            producto.nombre = data.get('nombre', producto.nombre)
            producto.precio = data.get('precio', producto.precio)
            producto.marca_id = data.get('marca_id', producto.marca_id)
            producto.rubro_id = data.get('rubro_id', producto.rubro_id)
            producto.tipo_id = data.get('tipo_id', producto.tipo_id)

            db.session.commit()
            return {'message': 'Producto actualizado exitosamente'}, 200
        else:
            producto.nombre = request.form['nombre']
            producto.precio = request.form['precio']
            producto.marca_id = request.form['marca_id']
            producto.rubro_id = request.form['rubro_id']
            producto.tipo_id = request.form['tipo_id']

            db.session.commit()
            flash('Producto actualizado exitosamente')
            return redirect(url_for('productos.listar_productos'))

    return render_template('editar_producto.html', producto=producto)


@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST', 'DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    if request.method == 'DELETE' or request.is_json:
        return {'message': 'Producto eliminado exitosamente'}, 200
    else:
        flash('Producto eliminado exitosamente')
        return redirect(url_for('productos.listar_productos'))


@productos_bp.route('/cargar_productos', methods=['POST'])
def cargar_productos():
    if 'file' not in request.files:
        flash('No se ha seleccionado ningún archivo.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    file = request.files['file']

    if file.filename == '':
        flash('No se ha seleccionado ningún archivo.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    if file and allowed_file(file.filename):
        # Leer el archivo Excel
        df = pd.read_excel(file)

        # Iterar sobre las filas y crear productos
        for index, row in df.iterrows():
            codigo1 = row['codigo1']
            nombre = row['nombre']
            costo = row['costo']
            precio = row['precio']

            # Validar si el producto ya existe
            if Producto.query.filter_by(codigo1=codigo1).first():
                continue  # Ignorar si ya existe

            nuevo_producto = Producto(
                codigo1=codigo1,
                nombre=nombre,
                costo=costo,
                precio=precio,
                stock=0  # Inicializar stock a 0 o lo que desees
            )
            db.session.add(nuevo_producto)

        db.session.commit()
        flash('Productos cargados exitosamente!', 'success')
    else:
        flash('Formato de archivo no permitido. Asegúrate de subir un archivo Excel.', 'danger')

    return redirect(url_for('productos.listar_productos'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']

@productos_bp.route('/productos/buscar', methods=['GET'])
def buscar_productos():
    query = request.args.get('q', '').strip()

    # Buscar productos cuyo nombre o código coincidan con el término de búsqueda
    productos = Producto.query.filter(
        db.or_(
            Producto.nombre.ilike(f'%{query}%'),
            Producto.codigo1.ilike(f'%{query}%')
        )
    ).limit(50).all()  # Limitar la cantidad de resultados para evitar sobrecarga

    return jsonify([producto.to_dict() for producto in productos])