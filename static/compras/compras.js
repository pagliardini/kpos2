const codigoInput = document.getElementById('codigo_producto');
const productosTabla = document.getElementById('productos_tabla');
const totalInput = document.getElementById('total');
const ivaInput = document.getElementById('iva');
const proveedorSelect = document.getElementById('proveedor_id');
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
            // Crear un campo para ingresar la cantidad
            const nuevaFila = `
                <tr data-costo="${data.costo}"> <!-- Guardamos el costo del producto en el dataset -->
                    <td>${data.codigo1}</td>
                    <td>${data.nombre}</td>
                    <td>${data.costo}</td>
                    <td>${data.stock}</td>
                    <td><input type="number" min="1" value="1" class="cantidad-input" /></td>
                </tr>
            `;
            productosTabla.innerHTML += nuevaFila;

            // Actualizar el total
            total += parseFloat(data.costo);
            totalInput.value = total.toFixed(2);

            // Limpiar el campo de código
            codigoInput.value = '';
            codigoInput.focus();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al buscar el producto');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos el campo de total
    const totalInput = document.getElementById('total');
    const productosTabla = document.getElementById('productos_tabla');

    // Funcion para recalcular el total
    function recalcularTotal() {
        let total = 0;

        // Recorremos cada fila de producto
        productosTabla.querySelectorAll('tr').forEach(row => {
            const cantidadInput = row.querySelector('.cantidad-input');
            const costoProducto = parseFloat(row.dataset.costo);  // Guardamos el costo del producto en el dataset

            // Si hay cantidad ingresada, multiplicamos por el costo del producto
            if (cantidadInput && cantidadInput.value) {
                const cantidad = parseInt(cantidadInput.value);
                if (!isNaN(cantidad)) {
                    total += cantidad * costoProducto;
                }
            }
        });

        // Actualizar el valor en el input de total
        totalInput.value = total.toFixed(2);
    }

    // Agregar el evento para los inputs de cantidad
    productosTabla.addEventListener('input', function (event) {
        if (event.target.classList.contains('cantidad-input')) {
            recalcularTotal();
            actualizarTotalConIva(); // Actualizamos el total con IVA cada vez que cambia la cantidad
        }
    });

    // Agregar el evento para el input de IVA
    ivaInput.addEventListener('input', function () {
        actualizarTotalConIva();
    });

    // Función para actualizar el total incluyendo el IVA
    function actualizarTotalConIva() {
        const iva = parseFloat(ivaInput.value) || 0;
        const subtotal = parseFloat(totalInput.value) || 0;
        const totalConIva = subtotal + iva;
        totalInput.value = totalConIva.toFixed(2);
    }

    // También podrías recalcular el total al cargar los productos por primera vez, si lo deseas.
    recalcularTotal();
});

// Evento para registrar la compra
document.getElementById('registrar_compra_btn').addEventListener('click', () => {
    registrarCompra();
});

function registrarCompra() {
    const proveedorId = proveedorSelect.value;
    const iva = parseFloat(ivaInput.value) || 0;
    const fechaCompraInput = document.getElementById('fecha_compra').value; // Obtén la fecha del input

    // Recopilar detalles de los productos
    const productosDetalles = [];
    const filas = productosTabla.getElementsByTagName('tr');

    let totalCompra = 0;

    for (let fila of filas) {
        const celdas = fila.getElementsByTagName('td');
        const productoId = celdas[0].innerText;
        const nombreProducto = celdas[1].innerText;
        const cantidadInput = celdas[4].querySelector('.cantidad-input');
        const cantidad = parseInt(cantidadInput.value) || 1;
        const precioUnitario = parseFloat(celdas[2].innerText);

        productosDetalles.push({
            producto_id: productoId,
            producto_nombre: nombreProducto,
            cantidad: cantidad,
            precio_unitario: precioUnitario,
        });

        // Calcular el total de la compra aquí
        totalCompra += cantidad * precioUnitario;
    }

    // Calcular el total incluyendo IVA
    const totalConIva = totalCompra + iva;

    // Enviar los datos a la ruta /procesar_compra
    fetch('/procesar_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_proveedor: proveedorId,
            iva: iva,
            total: totalConIva,
            detalles: productosDetalles,
            fecha_compra: fechaCompraInput // Asegúrate de enviar la fecha aquí
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
