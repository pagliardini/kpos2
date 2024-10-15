const codigoInput = document.getElementById('codigo_producto');
const productosTabla = document.getElementById('productos_tabla');
const totalInput = document.getElementById('total');
const ivaInput = document.getElementById('iva'); // Referencia al input de IVA
const proveedorSelect = document.getElementById('proveedor_id'); // Referencia al select de proveedor
let total = 0;

codigoInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        buscarProducto();
    }
});

function buscarProducto() {
    const codigo = codigoInput.value;

    fetch('/buscar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ codigo: codigo }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const nuevaFila = `
                <tr>
                    <td>${data.codigo1}</td>
                    <td>${data.nombre}</td>
                    <td>${data.costo}</td>
                    <td>${data.stock}</td>
                    <td>1</td>
                </tr>
            `;
            productosTabla.innerHTML += nuevaFila;

            total += parseFloat(data.costo);
            totalInput.value = total.toFixed(2);

            codigoInput.value = '';
            codigoInput.focus();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al buscar el producto');
    });
}

// Evento para registrar la compra
document.getElementById('registrar_compra_btn').addEventListener('click', () => {
    registrarCompra();
});

function registrarCompra() {
    const proveedorId = proveedorSelect.value;
    const iva = parseFloat(ivaInput.value) || 0; // Asegúrate de que sea un número
    const totalCompra = parseFloat(totalInput.value) || 0;

    // Calcular el total incluyendo IVA
    const totalConIva = totalCompra + iva;

    // Recopilar detalles de los productos
    const productosDetalles = [];
    const filas = productosTabla.getElementsByTagName('tr');

    for (let fila of filas) {
        const celdas = fila.getElementsByTagName('td');
        const productoId = celdas[0].innerText; // Suponiendo que el código es el ID del producto
        const nombreProducto = celdas[1].innerText;
        const cantidad = parseInt(celdas[4].innerText); // Cantidad fija en 1
        const precioUnitario = parseFloat(celdas[2].innerText);

        productosDetalles.push({
            producto_id: productoId,
            producto_nombre: nombreProducto,
            cantidad: cantidad,
            precio_unitario: precioUnitario,
        });
    }

    // Enviar los datos a la ruta /procesar_compra
    fetch('/procesar_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_proveedor: proveedorId,
            iva: iva,
            total: totalConIva,  // Usar el total con IVA aquí
            detalles: productosDetalles,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Compra registrada exitosamente');
            // Limpiar la tabla y los campos después de registrar
            productosTabla.innerHTML = '';
            total = 0;
            totalInput.value = '';
            ivaInput.value = '';
            proveedorSelect.value = '';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al registrar la compra');
    });
}