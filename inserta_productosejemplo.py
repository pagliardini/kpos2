from app import create_app
from extensions import db
from models.producto import Producto

# Crea la aplicación
app = create_app()

# Insertar datos en la base de datos
with app.app_context():
    # Crear productos de ejemplo
    productos = [
        {"nombre": "VAPER HQD2000", "precio": 50.99, "codigo1": "6937105412541"},
        {"nombre": "CURITAS", "precio": 25.49, "codigo1": "7702003010743"},
        {"nombre": "BROCHER GRAP 1000", "precio": 150.00, "codigo1": "7798006050084"},
        {"nombre": "BATERIA 18650", "precio": 12.99, "codigo1": "1234567890123"},
        {"nombre": "CARGADOR USB", "precio": 15.49, "codigo1": "9876543210987"},
        {"nombre": "VAPE JUICE MANGO", "precio": 22.99, "codigo1": "1111111111111"},
        {"nombre": "VAPE JUICE FRESA", "precio": 22.99, "codigo1": "2222222222222"},
        {"nombre": "VAPE JUICE MENTA", "precio": 22.99, "codigo1": "3333333333333"},
        {"nombre": "PAPEL DE LENTICULAR", "precio": 5.99, "codigo1": "4444444444444"},
        {"nombre": "FILTRO DE AGUA", "precio": 29.99, "codigo1": "5555555555555"},
        {"nombre": "LAMPARA LED", "precio": 35.00, "codigo1": "6666666666666"},
        {"nombre": "MOUSE GAMER", "precio": 45.00, "codigo1": "7777777777777"},
        {"nombre": "TECLADO MECANICO", "precio": 75.00, "codigo1": "8888888888888"},
        {"nombre": "WEBCAM HD", "precio": 60.00, "codigo1": "9999999999999"},
        {"nombre": "MICROFONO USB", "precio": 40.00, "codigo1": "1010101010101"},
        {"nombre": "PARLANTE BLUETOOTH", "precio": 55.00, "codigo1": "2020202020202"},
        {"nombre": "POWER BANK 10000mAh", "precio": 25.00, "codigo1": "3030303030303"},
        {"nombre": "CABLE HDMI", "precio": 10.00, "codigo1": "4040404040404"},
        {"nombre": "ADAPTADOR USB-C", "precio": 12.50, "codigo1": "5050505050505"},
        {"nombre": 'SOPORTE PARA TELEFONO', 'precio': 8.99, 'codigo1': '6060606060606'},
    ]

    # Agregar productos a la sesión de la base de datos
    for producto in productos:
        nuevo_producto = Producto(nombre=producto["nombre"], precio=producto["precio"], codigo1=producto["codigo1"])
        db.session.add(nuevo_producto)

    # Confirmar los cambios (insertar los productos en la base de datos)
    db.session.commit()

print("Productos insertados correctamente.")
