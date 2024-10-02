from extensions import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    # Aquí puedes agregar una relación con el modelo Producto si es necesario
