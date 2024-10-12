from .productos import productos_bp
from .rubros import rubros_bp
from .marcas import marcas_bp
from .tipos import tipos_bp

def register_productos_blueprints(app):
    app.register_blueprint(productos_bp)
    app.register_blueprint(rubros_bp)
    app.register_blueprint(marcas_bp)
    app.register_blueprint(tipos_bp)
