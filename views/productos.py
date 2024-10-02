from flask import Blueprint, render_template
from models.producto import Producto
from extensions import db

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)
