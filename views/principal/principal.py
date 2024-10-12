from flask import Blueprint, render_template


principal_bp = Blueprint('principal', __name__)

# Ruta para mostrar todos los productos
@principal_bp.route('/')
def principal():
    return render_template('index.html')

