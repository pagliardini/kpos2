// productos.js
let productosSeleccionados = [];

function agregarProductoPorCodigo(codigo) {
    fetch(`/buscar_producto?codigo=${codigo}`)
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
                alert("Producto no encontrado");
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
            <li>
                <span class="producto-nombre">${producto.nombre} - $${producto.precio}</span>
                <div class="cantidad-control">
                    <button onclick="actualizarCantidad(${producto.id}, ${producto.cantidad - 1})">&#x25BC;</button>
                    <span>${producto.cantidad}</span>
                    <button onclick="actualizarCantidad(${producto.id}, ${producto.cantidad + 1})">&#x25B2;</button>
                </div>
                <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
            </li>
        `;
    });
    document.getElementById('total').innerText = 'Total: $' + total.toFixed(2);
}

function actualizarCantidad(id, nuevaCantidad) {
    const producto = productosSeleccionados.find(p => p.id === id);
    if (producto) {
        producto.cantidad = parseInt(nuevaCantidad);
        actualizarListaProductos();
    }
}

function eliminarProducto(id) {
    productosSeleccionados = productosSeleccionados.filter(p => p.id !== id);
    actualizarListaProductos();
}
