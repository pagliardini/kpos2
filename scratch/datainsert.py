from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar los modelos (asegúrate de que estos estén definidos como en tus ejemplos anteriores)
from extensions import db
from models import (Factura, FacturaDetalle, Marca, Proveedor,
                    Compra, CompraDetalle, Rubro, Tipo, Producto)

# Crear la base de datos (ajusta la URL según tu configuración)
engine = create_engine('sqlite:///mi_base_de_datos.db')  # Cambia la ruta según sea necesario
db.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insertar datos en la tabla marcas
marca1 = Marca(nombre='Marca A')
marca2 = Marca(nombre='Marca B')
session.add_all([marca1, marca2])

# Insertar datos en la tabla rubros
rubro1 = Rubro(nombre='Rubro A')
rubro2 = Rubro(nombre='Rubro B')
session.add_all([rubro1, rubro2])

# Insertar datos en la tabla tipos
tipo1 = Tipo(nombre='Tipo A')
tipo2 = Tipo(nombre='Tipo B')
session.add_all([tipo1, tipo2])

# Insertar datos en la tabla proveedores
proveedor1 = Proveedor(cuit='20-12345678-9', nombre='Proveedor A',
                       telefono='123456789', direccion='Calle 1',
                       email='proveedorA@example.com',
                       fecha_creacion=datetime.utcnow())
proveedor2 = Proveedor(cuit='20-98765432-1', nombre='Proveedor B',
                       telefono='987654321', direccion='Calle 2',
                       email='proveedorB@example.com',
                       fecha_creacion=datetime.utcnow())
session.add_all([proveedor1, proveedor2])

# Insertar datos en la tabla productos
producto1 = Producto(nombre='Producto A', costo=10.0, precio=15.0,
                     codigo1='P001', stock=100,
                     marca_id=1, rubro_id=1, tipo_id=1)
producto2 = Producto(nombre='Producto B', costo=20.0, precio=30.0,
                     codigo1='P002', stock=50,
                     marca_id=2, rubro_id=2, tipo_id=2)
session.add_all([producto1, producto2])

# Insertar datos en la tabla facturas
factura1 = Factura(fecha=datetime.utcnow(), total=150.0)
factura2 = Factura(fecha=datetime.utcnow(), total=300.0)
session.add_all([factura1, factura2])

# Insertar datos en la tabla facturas_detalles
detalle1 = FacturaDetalle(factura_id=1, producto_id=1,
                           producto_nombre='Producto A', cantidad=5,
                           precio_unitario=15.0)
detalle2 = FacturaDetalle(factura_id=1, producto_id=2,
                           producto_nombre='Producto B', cantidad=3,
                           precio_unitario=30.0)
session.add_all([detalle1, detalle2])

# Insertar datos en la tabla compras
compra1 = Compra(id_proveedor=1, fecha_carga=datetime.utcnow(), iva=21.0, total=200.0)
compra2 = Compra(id_proveedor=2, fecha_carga=datetime.utcnow(), iva=21.0, total=400.0)
session.add_all([compra1, compra2])

# Insertar datos en la tabla compras_detalles
detalle_compra1 = CompraDetalle(compra_id=1, producto_id=1,
                                 producto_nombre='Producto A', cantidad=10,
                                 precio_unitario=10.0)
detalle_compra2 = CompraDetalle(compra_id=2, producto_id=2,
                                 producto_nombre='Producto B', cantidad=5,
                                 precio_unitario=20.0)
session.add_all([detalle_compra1, detalle_compra2])

# Confirmar los cambios y cerrar la sesión
session.commit()
session.close()

print("Datos de ejemplo insertados correctamente.")