from .principal import principal_bp


def register_principal_blueprints(app):
    app.register_blueprint(principal_bp)