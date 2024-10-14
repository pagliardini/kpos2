// modal.js
let productosEncontrados = [];
let indiceSeleccionado = -1;

function mostrarModal() {
    console.log('Mostrando modal');
    document.getElementById('modal-buscar').style.display = 'block';
    document.getElementById('descripcion').value = '';
    document.getElementById('resultado-busqueda').innerHTML = '';
    document.getElementById('descripcion').focus();
}

function cerrarModal() {
    document.getElementById('modal-buscar').style.display = 'none';
}

function buscarProductoPorDescripcion() {
    const descripcion = document.getElementById('descripcion').value;
    if (descripcion.length > 0) {
        fetch(`/buscar_producto_descripcion?descripcion=${descripcion}`)
            .then(response => response.json())
            .then(productos => {
                productosEncontrados = productos.slice(0, 15);
                const resultados = document.getElementById('resultado-busqueda');
                resultados.innerHTML = '';
                productosEncontrados.forEach((producto, index) => {
                    const li = document.createElement('li');
                    li.textContent = `${producto.nombre} - $${producto.precio}`;
                    li.dataset.index = index;
                    li.onclick = () => agregarProductoPorId(producto.id);
                    resultados.appendChild(li);
                });
                indiceSeleccionado = -1;
            });
    } else {
        document.getElementById('resultado-busqueda').innerHTML = '';
    }
}

document.getElementById('descripcion').addEventListener('keydown', function(event) {
    const resultados = document.getElementById('resultado-busqueda');
    const items = resultados.getElementsByTagName('li');

    if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (indiceSeleccionado < items.length - 1) {
            indiceSeleccionado++;
            resaltarProductoSeleccionado(items);
        }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (indiceSeleccionado > 0) {
            indiceSeleccionado--;
            resaltarProductoSeleccionado(items);
        }
    } else if (event.key === 'Enter') {
        event.preventDefault();
        if (indiceSeleccionado >= 0 && indiceSeleccionado < productosEncontrados.length) {
            agregarProductoPorId(productosEncontrados[indiceSeleccionado].id);
        }
    }
});

function resaltarProductoSeleccionado(items) {
    for (let i = 0; i < items.length; i++) {
        items[i].classList.remove('selected');
    }
    if (indiceSeleccionado >= 0 && indiceSeleccionado < items.length) {
        items[indiceSeleccionado].classList.add('selected');
    }
}

function agregarProductoPorId(idProducto) {
    fetch(`/buscar_producto_por_id?id=${idProducto}`)
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
            }
            cerrarModal();
            document.getElementById('codigo').focus();  // Vuelve a enfocar el campo de código
        });
}
