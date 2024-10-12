from .caja import caja_bp

def register_caja_blueprints(app):
    app.register_blueprint(caja_bp)