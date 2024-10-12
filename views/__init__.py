from flask import Blueprint

# Inicializa los blueprints aquí si es necesario.
ventas_bp = Blueprint('ventas', __name__)
compras_bp = Blueprint('compras', __name__)
caja_bp = Blueprint('caja', __name__)
productos_bp = Blueprint('productos', __name__)

# Importa las rutas después de definir los blueprints.
from .ventas import *
from .compras import *
from .caja import *
from .productos import *