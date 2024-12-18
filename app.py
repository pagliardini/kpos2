from flask import Flask
from config import Config
from extensions import db
from views.ventas import ventas_bp
from views.principal import principal_bp
from views.compras import compras_bp
from views.caja import caja_bp
from views.productos import register_productos_blueprints
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)
    app.secret_key = 'clave_secreta_random'
    app.config.from_object(Config)

    db.init_app(app)

    # Registramos los blueprints
    app.register_blueprint(ventas_bp)
    app.register_blueprint(principal_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(caja_bp)

    register_productos_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

