let indiceSeleccionadoFactura = -1; // Inicializamos en -1 para indicar que ningún producto está seleccionado al inicio

document.addEventListener('keydown', function(event) {
    const listaProductos = document.getElementById('lista-productos');
    const filas = listaProductos.getElementsByTagName('tr');

    const modalAbierto = document.getElementById('modal-buscar').style.display === 'block';

    if (!modalAbierto && filas.length > 0) {
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            if (indiceSeleccionadoFactura === -1 || indiceSeleccionadoFactura >= filas.length - 1) {
                indiceSeleccionadoFactura = 0; // Ir al primer producto
            } else {
                indiceSeleccionadoFactura++;
            }
            resaltarProductoSeleccionadoFactura(filas);
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            if (indiceSeleccionadoFactura <= 0) {
                indiceSeleccionadoFactura = filas.length - 1; // Ir al último producto
            } else {
                indiceSeleccionadoFactura--;
            }
            resaltarProductoSeleccionadoFactura(filas);
        }
    }
});

function resaltarProductoSeleccionadoFactura(filas) {
    for (let i = 0; i < filas.length; i++) {
        filas[i].classList.remove('selected');
    }
    if (indiceSeleccionadoFactura >= 0 && indiceSeleccionadoFactura < filas.length) {
        filas[indiceSeleccionadoFactura].classList.add('selected');
    }
}