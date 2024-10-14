document.getElementById('buscar').addEventListener('click', function () {
    const codigo = document.getElementById('codigo').value;
    buscarProducto(codigo);
});

function buscarProducto(codigo) {
    fetch(`/buscar_producto?codigo=${codigo}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la búsqueda del producto');
            }
            return response.json();
        })
        .then(producto => {
            if (producto) {
                mostrarProducto(producto);
            } else {
                alert("Producto no encontrado");
            }
        })
        .catch(error => {
            console.error('Error al buscar el producto:', error);
            alert("Error al buscar el producto: " + error.message);
        });
}

function mostrarProducto(producto) {
    console.log(producto)
    // Asumiendo que tienes un elemento para mostrar la info del producto
    const productoInfo = document.getElementById('producto-info');

    // Asegúrate de que los valores estén definidos y sean números antes de usar toFixed
    const costo = producto.costo !== undefined ? producto.costo : 0.00;

    productoInfo.innerHTML = `
        <p>ID: ${producto.id}</p>
        <p>Producto: ${producto.nombre}</p>
        <p>Costo Unitario: $${costo.toFixed(2)}</p>
    `;
}
