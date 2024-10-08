// venta.js
function procesarVenta() {
    const idsProductos = productosSeleccionados.map(p => ({ id: p.id, cantidad: p.cantidad }));

    fetch(urlProcesarVenta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productos: idsProductos })
    }).then(() => {
        alert('Venta procesada con éxito');
        window.location.reload();
    }).catch((error) => {
        console.error('Error procesando la venta:', error);
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
