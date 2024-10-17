// productos.js
let productosSeleccionados = [];

function agregarProductoPorCodigo(codigo) {
    fetch(`/ventas/buscar/codigo?codigo=${codigo}`)
        .then(response => response.json())
        .then(producto => {
            if (producto) {
                const existe = productosSeleccionados.find(p => p.id === producto.id);
                if (!existe) {
                    producto.cantidad = 1;
                    productosSeleccionados.push(producto);
                } else {
                    existe.cantidad += 1;
                }
                actualizarListaProductos();
            } else {
                // Usar Toastify para mostrar el mensaje de error
                Toastify({
                    text: `Producto no encontrado: El código ${codigo} no existe en el sistema.`,
                    duration: 3000, // Duración en milisegundos
                    gravity: "top", // top or bottom
                    position: 'right', // left, center or right
                    backgroundColor: "linear-gradient(to right, #FF5F6D, #FFC371)", // Color de fondo
                }).showToast();
            }
            document.getElementById('codigo').value = '';
            document.getElementById('codigo').focus();
        })
        .catch(error => {
            console.error('Error al buscar el producto:', error);
        });
}

function actualizarListaProductos() {
    const lista = document.getElementById('lista-productos');
    lista.innerHTML = '';
    let total = 0;

    productosSeleccionados.forEach(producto => {
        total += producto.precio * producto.cantidad;
        lista.innerHTML += `
            <tr>
                <td class="py-2 px-4">${producto.id}</td>
                <td class="py-2 px-4">${producto.nombre}</td>
                <td class="py-2 px-4 text-right">
                    <button onclick="actualizarCantidad(${producto.id}, ${producto.cantidad - 1})">&#x25BC;</button>
                    <span>${producto.cantidad}</span>
                    <button onclick="actualizarCantidad(${producto.id}, ${producto.cantidad + 1})">&#x25B2;</button>
                </td>
                <td class="py-2 px-4 text-right">$${producto.precio.toFixed(2)}</td>
                <td class="py-2 px-4 text-right">$${(producto.precio * producto.cantidad).toFixed(2)}</td>
                <td class="py-2 px-4 text-center">
                    <button onclick="eliminarProducto(${producto.id})" class="text-red-600">Eliminar</button>
                </td>
            </tr>
        `;
    });

    document.getElementById('total').innerText = 'Total: $' + total.toFixed(2);
}

function actualizarCantidad(id, nuevaCantidad) {
    const producto = productosSeleccionados.find(p => p.id === id);
    if (producto) {
        producto.cantidad = parseInt(nuevaCantidad);
        if (producto.cantidad <= 0) {
            eliminarProducto(id);
        } else {
            actualizarListaProductos();
        }
    }
}

function eliminarProducto(id) {
    productosSeleccionados = productosSeleccionados.filter(p => p.id !== id);
    actualizarListaProductos();
}
