import pymssql
import sqlite3
from decimal import Decimal


sql_server_conn = pymssql.connect(
    server='',
    user='',
    password='',
    database=''
)

sqlite_conn = sqlite3.connect('punto_de_venta.db')
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS Productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    codigo1 TEXT NOT NULL
)
''')

sql_query = "SELECT Id_Producto, Descripcion, Precio_Venta FROM Productos"
with sql_server_conn.cursor() as cursor:
    cursor.execute(sql_query)
    rows = cursor.fetchall()


for row in rows:
    codigo1 = str(row[0])
    nombre = row[1]
    precio = float(row[2]) if isinstance(row[2], Decimal) else row[2]

    sqlite_cursor.execute('''
    INSERT INTO Productos (nombre, precio, codigo1) VALUES (?, ?, ?)
    ''', (nombre, precio, codigo1))

sqlite_conn.commit()
sqlite_conn.close()
sql_server_conn.close()

print("Datos copiados exitosamente de SQL Server a SQLite.")