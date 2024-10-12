from .compras import compras_bp


def register_compras_blueprints(app):
    app.register_blueprint(compras_bp)