



# rtar datos de ejemplo en la tabla Productos
sqlite_cursor.execute('''
INSERT INTO productos (nombre, precio, codigo1, marca_id, rubro_id, tipo_id, stock) VALUES 
('Producto A', 100.50, 'A001', 1, 1, 1, 0),
('Producto B', 200.00, 'A002', 2, 2, 2, 0),
('Producto C', 150.75, 'A003', 3, 3, 3, 0)
''')