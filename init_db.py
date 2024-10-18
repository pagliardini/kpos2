from app import create_app
from extensions import db
from datetime import datetime, timezone

# Importar los modelos
from models import (Factura, FacturaDetalle, Marca, Proveedor,
                    Compra, CompraDetalle, Rubro, Tipo, Producto,
                    Cliente, FormaCobro)

app = create_app()

with app.app_context():
    # Crear las tablas
    db.create_all()

    # Insertar datos en la tabla marcas
    marca1 = Marca(nombre='Marca A')
    marca2 = Marca(nombre='Marca B')
    db.session.add_all([marca1, marca2])

    # Insertar datos en la tabla rubros
    rubro1 = Rubro(nombre='Rubro A')
    rubro2 = Rubro(nombre='Rubro B')
    db.session.add_all([rubro1, rubro2])

    # Insertar datos en la tabla tipos
    tipo1 = Tipo(nombre='Tipo A')
    tipo2 = Tipo(nombre='Tipo B')
    db.session.add_all([tipo1, tipo2])

    # Insertar datos en la tabla proveedores
    proveedor1 = Proveedor(
        cuit='20-12345678-9',
        nombre='Proveedor A',
        telefono='123456789',
        direccion='Calle 1',
        email='proveedorA@example.com',
        fecha_creacion=datetime.now(timezone.utc)  # Cambiado aquí
    )
    proveedor2 = Proveedor(
        cuit='20-98765432-1',
        nombre='Proveedor B',
        telefono='987654321',
        direccion='Calle 2',
        email='proveedorB@example.com',
        fecha_creacion=datetime.now(timezone.utc)  # Cambiado aquí
    )
    db.session.add_all([proveedor1, proveedor2])

    # Insertar datos en la tabla productos
    producto1 = Producto(
        nombre='Producto A',
        costo=10.0,
        precio=15.0,
        codigo1='P001',
        stock=100,
        marca_id=1,
        rubro_id=1,
        tipo_id=1
    )
    producto2 = Producto(
        nombre='Producto B',
        costo=20.0,
        precio=30.0,
        codigo1='P002',
        stock=50,
        marca_id=2,
        rubro_id=2,
        tipo_id=2
    )
    db.session.add_all([producto1, producto2])

    # Insertar datos en la tabla facturas
    factura1 = Factura(fecha=datetime.now(timezone.utc), total=150.0)  # Cambiado aquí
    factura2 = Factura(fecha=datetime.now(timezone.utc), total=300.0)  # Cambiado aquí
    db.session.add_all([factura1, factura2])

    # Insertar datos en la tabla facturas_detalles
    detalle1 = FacturaDetalle(factura_id=1, producto_id=1,
                               producto_nombre='Producto A', cantidad=5,
                               precio_unitario=15.0)
    detalle2 = FacturaDetalle(factura_id=1, producto_id=2,
                               producto_nombre='Producto B', cantidad=3,
                               precio_unitario=30.0)
    db.session.add_all([detalle1, detalle2])

    # Insertar datos en la tabla compras
    compra1 = Compra(id_proveedor=1, fecha_carga=datetime.now(timezone.utc), iva=21.0, total=200.0)  # Cambiado aquí
    compra2 = Compra(id_proveedor=2, fecha_carga=datetime.now(timezone.utc), iva=21.0, total=400.0)  # Cambiado aquí
    db.session.add_all([compra1, compra2])

    # Insertar datos en la tabla compras_detalles
    detalle_compra1 = CompraDetalle(compra_id=1, producto_id=1,
                                     producto_nombre='Producto A', cantidad=10,
                                     precio_unitario=10.0)
    detalle_compra2 = CompraDetalle(compra_id=2, producto_id=2,
                                     producto_nombre='Producto B', cantidad=5,
                                     precio_unitario=20.0)
    db.session.add_all([detalle_compra1, detalle_compra2])

    # Tabla clientes

    cliente1 = Cliente(id=1, nombre='Consumidor', apellido='Final', numero=99999999)
    cliente2 = Cliente(id=2, nombre='Alan', apellido='Garcia', numero=35917637)
    db.session.add_all([cliente1, cliente2])

    # Formas de cobro

    fcobro1 = FormaCobro(id=1, denominacion='Efectivo', recargo=0.0)
    fcobro2 = FormaCobro(id=2, denominacion='Mercado Pago', recargo=0.0)
    fcobro3 = FormaCobro(id=3, denominacion='Débito', recargo=7.0)
    fcobro4 = FormaCobro(id=4, denominacion='Crédito', recargo=15)
    db.session.add_all([fcobro1, fcobro2, fcobro3, fcobro4])

    # Confirmar los cambios y cerrar la sesión
    db.session.commit()

print("Base de datos inicializada y datos de ejemplo insertados correctamente.")
