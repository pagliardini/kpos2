from extensions import db


class FacturaDetalle(db.Model):
    __tablename__ = 'facturas_detalle'

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'),
                            nullable=False)  # Asegúrate de que el nombre de la tabla productos sea correcto
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relación con el modelo Factura
    factura = db.relationship('Factura', back_populates='detalles')

    # Relación con el modelo Producto (si lo tienes)
    producto = db.relationship('Producto', back_populates='detalles')  # Descomentar si tienes un modelo Producto


# Agregar la relación en el modelo Factura
Factura.detalles = db.relationship('FacturaDetalle', back_populates='factura', cascade='all, delete-orphan')
