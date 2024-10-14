from datetime import datetime
from extensions import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cuit = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.String(40), nullable=True)
    direccion = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    # Fechas
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Valor por defecto
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Actualiza automáticamente
