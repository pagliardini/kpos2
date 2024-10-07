from flask import Flask
from config import Config
from extensions import db
from views.ventas import ventas_bp
from views.productos import productos_bp
from views.principal import principal_bp



def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = 'clave_secreta_random'  # Clave secreta
    app.config.from_object(Config)

    # Inicializamos SQLAlchemy
    db.init_app(app)

    # Registramos los blueprints
    app.register_blueprint(ventas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(principal_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
