from .ventas import ventas_bp

def register_ventas_blueprints(app):
    app.register_blueprint(ventas_bp)