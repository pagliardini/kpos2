from extensions import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)  # Cambiado a datetime.utcnow
    iva = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)


class CompraDetalle(db.Model):
    __tablename__ = 'compras_detalles'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    producto_nombre = db.Column(db.String(50), nullable=False)  # Almacenar el nombre del producto
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
