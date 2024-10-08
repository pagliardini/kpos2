import requests

url = 'http://localhost:5000/api/agregar_producto'
headers = {'Content-Type': 'application/json'}
data = {
    "nombre": "Nuevo Producto",
    "precio": 10.99,
    "codigo": "ABC123",
    "marca_id": 1,
    "rubro_id": 2,
    "tipo_id": 3
}

response = requests.post(url, json=data, headers=headers)

# Verificar la respuesta
if response.status_code == 201:
    print("Producto agregado exitosamente:", response.json())
else:
    print("Error:", response.status_code, response.json())
