from app import create_app
from extensions import db
from models.producto import Producto

# Crea la aplicación
app = create_app()

# Insertar datos en la base de datos
with app.app_context():
    # Crear 3 productos de ejemplo
    producto1 = Producto(nombre="Teclado Mecánico", precio=50.99)
    producto2 = Producto(nombre="Mouse Inalámbrico", precio=25.49)
    producto3 = Producto(nombre="Monitor 24 pulgadas", precio=150.00)

    # Agregar productos a la sesión de la base de datos
    db.session.add(producto1)
    db.session.add(producto2)
    db.session.add(producto3)

    # Confirmar los cambios (insertar los productos en la base de datos)
    db.session.commit()

print("Productos insertados correctamente.")
