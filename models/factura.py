from pickle import FALSE

from extensions import db
from datetime import datetime


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=True)


class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    forma_cobro_id = db.Column(db.Integer, db.ForeignKey('formas_cobro.id'), nullable=False)  # Referencia a FormaCobro
    forma_cobro = db.relationship('FormaCobro', backref='facturas')  # Relación con FormaCobro

class FacturaDetalle(db.Model):
    __tablename__ = 'facturas_detalles'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    producto_nombre = db.Column(db.String(50), nullable=False)  # Almacenar el nombre del producto
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

class FormaCobro(db.Model):
    __tablename__ = 'formas_cobro'
    id = db.Column(db.Integer, primary_key=True)
    denominacion = db.Column(db.String(50), nullable=False)
    recargo = db.Column(db.Float, nullable=False)
    es_default = db.Column(db.Boolean, nullable=False, default=False)
