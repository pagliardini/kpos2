from extensions import db

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='marca', lazy=True)

class Rubro(db.Model):
    __tablename__ = 'rubros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='rubro', lazy=True)

class Tipo(db.Model):
    __tablename__ = 'tipos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='tipo', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    codigo1 = db.Column(db.String(50), nullable=False)

    # Claves foráneas para relacionar Producto con Marca, Rubro y Tipo
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubros.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos.id'), nullable=False)
