from flask import Flask
from config import Config
from extensions import db
from views.ventas import ventas_bp
from views.principal import principal_bp
from views.compras import compras_bp
from views.caja import caja_bp
from views.productos import register_productos_blueprints  # Importar la función de productos modularizada


def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'clave_secreta_random'  # Clave secreta
    app.config.from_object(Config)

    # Inicializamos SQLAlchemy
    db.init_app(app)

    # Registramos los blueprints
    app.register_blueprint(ventas_bp)
    app.register_blueprint(principal_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(caja_bp)

    # Registrar blueprints de productos desde la función modularizada
    register_productos_blueprints(app)

    return app


if __name__ == '__main__':
    app = create_app()
