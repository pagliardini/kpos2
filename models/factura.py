from extensions import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    # Aquí puedes agregar una relación con el modelo Producto si es necesario

class FacturaDetalle(db.Model):
    __tablename__ = 'facturas_detalles'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    producto_nombre = db.Column(db.String(50), nullable=False)  # Almacenar el nombre del producto
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
