from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/proxy/pricely/<ean>', methods=['GET'])
def proxy_pricely(ean):
    try:
        # Hacer la solicitud a Pricely
        url = f"https://pricely.ar/product/{ean}"
        response = requests.get(url)
        response.raise_for_status()  # Verifica que el estado HTTP sea 200

        # Analizar el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el nombre del producto
        nombre_producto = soup.select_one(
            "body > main > div > div.max-w-5xl.w-full.bg-white.p-8.md\\:p-4.shadow-xl.mb-8 > div.flex.items-center.md\\:flex-row.gap-4.w-full.flex-col.md\\:p-4 > div.flex.flex-col.justify-center > h1"
        )
        nombre_producto = nombre_producto.text.strip() if nombre_producto else "Nombre no encontrado"

        # Extraer el precio promedio
        precio_promedio = soup.select_one(
            "body > main > div > div.max-w-5xl.w-full.bg-white.p-8.md\\:p-4.shadow-xl.mb-8 > div.md\\:p-4.mt-4 > div > div > div.flex.flex-col.md\\:flex-row.items-center.justify-between.gap-4.mt-8 > div > h3"
        )
        precio_promedio = precio_promedio.text.strip() if precio_promedio else "Precio no encontrado"

        # Retornar la información como JSON
        return jsonify({
            "nombre": nombre_producto,
            "precio": precio_promedio
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al conectarse con Pricely", "details": str(e)}), 500
    except AttributeError:
        return jsonify({"error": "No se pudo extraer información del producto."}), 500

if __name__ == '__main__':
    app.run(debug=True)
