import sqlite3

# Conexión a SQLite
sqlite_conn = sqlite3.connect('punto_de_venta.db')
sqlite_cursor = sqlite_conn.cursor()

# Insertar datos de ejemplo en la tabla Marcas
sqlite_cursor.execute('''
INSERT INTO Marcas (nombre) VALUES 
('Marca A'),
('Marca B'),
('Marca C')
''')

# Insertar datos de ejemplo en la tabla Rubros
sqlite_cursor.execute('''
INSERT INTO Rubros (nombre) VALUES 
('Rubro A'),
('Rubro B'),
('Rubro C')
''')

# Insertar datos de ejemplo en la tabla Tipos
sqlite_cursor.execute('''
INSERT INTO Tipos (nombre) VALUES 
('Tipo A'),
('Tipo B'),
('Tipo C')
''')

# Insertar datos de ejemplo en la tabla Productos
sqlite_cursor.execute('''
INSERT INTO Productos (nombre, costo, precio, codigo1, marca_id, rubro_id, tipo_id, stock) VALUES 
('Producto A', 0, 100.50, 'A001', 1, 1, 1, 1),
('Producto B', 0, 200.00, 'A002', 2, 2, 2, 2),
('Producto C', 0, 150.75, 'A003', 3, 3, 3, 55)
''')

# Insertar datos de ejemplo en la tabla Facturas_Detalles


# Guardar cambios y cerrar conexión
sqlite_conn.commit()
sqlite_conn.close()

print("Datos de ejemplo insertados en SQLite.")
