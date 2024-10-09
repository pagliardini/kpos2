from extensions import db

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='marca', lazy=True)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Rubro(db.Model):
    __tablename__ = 'rubros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='rubro', lazy=True)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Tipo(db.Model):
    __tablename__ = 'tipos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación uno a muchos con Producto
    productos = db.relationship('Producto', backref='tipo', lazy=True)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    costo = db.Column(db.Float, nullable=False, default=0.0)
    precio = db.Column(db.Float, nullable=False)
    codigo1 = db.Column(db.String(50), nullable=False)
    # Columna para manejar el stock (no nullable)
    stock = db.Column(db.Integer, nullable=False, default=0)


    # Claves foráneas para relacionar Producto con Marca, Rubro y Tipo
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id', ondelete='SET NULL'), nullable=True)
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubros.id', ondelete='SET NULL'), nullable=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos.id', ondelete='SET NULL'), nullable=True)



    # Método para serializar a un diccionario
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}