// venta.js
function procesarCompra() {
    const idsProductos = productosSeleccionados.map(p => ({ id: p.id, cantidad: p.cantidad }));
    console.log("Productos enviados para la venta:", idsProductos);  // Log para verificar cantidades

    fetch(urlProcesarCompra, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productos: idsProductos })
    }).then(() => {
        alert('Compra procesada con éxito');
        window.location.reload();
    }).catch((error) => {
        console.error('Error procesando la compra:', error);
    });
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'F6') {
        event.preventDefault();
        mostrarModal();
    } else if (event.key === 'Escape') {
        cerrarModal();
    }
});
