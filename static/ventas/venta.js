// venta.js
function procesarVenta() {
    const idsProductos = productosSeleccionados.map(p => ({ id: p.id, cantidad: p.cantidad }));
    console.log("Productos enviados para la venta:", idsProductos);

    fetch(urlProcesarVenta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productos: idsProductos })
    }).then(() => {
        // Mostrar notificación de éxito con Toastify
        Toastify({
            text: "La venta ha sido procesada con éxito.",
            duration: 1300,
            gravity: "bottom",
            position: 'left',
            backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();

        // Recargar la página después de un pequeño retraso
        setTimeout(() => {
            window.location.reload();
        }, 1300);
    }).catch((error) => {
        console.error('Error procesando la venta:', error);

        // Mostrar notificación de error con Toastify
        Toastify({
            text: "Ocurrió un error al procesar la venta. Inténtalo de nuevo.",
            duration: 3000,
            gravity: "bottom",
            position: 'left',
            backgroundColor: "linear-gradient(to right, #FF5F6D, #FFC371)",
        }).showToast();
    });
}

// Listener para el campo de código
document.getElementById('codigo').addEventListener('keydown', function(event) {
    const codigoInput = document.getElementById('codigo').value.trim();

    if (event.key === 'Enter') {
        event.preventDefault();

        if (codigoInput === '' && productosSeleccionados.length > 0) {
            procesarVenta();  // Procesa la venta si hay productos seleccionados
        } else if (codigoInput !== '') {
            agregarProductoPorCodigo(codigoInput);  // Agrega producto por código
        }
    }
});
document.addEventListener('keydown', function(event) {
    if (event.key === 'F6') {
        event.preventDefault();
        mostrarModal();
    } else if (event.key === 'Escape') {
        cerrarModal();
    }
});
