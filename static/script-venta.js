// Al cargar la página, establece el foco en el input de código
window.onload = function() {
    document.getElementById('codigo').focus();
};

let productosSeleccionados = [];

// Función para agregar un producto por código
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

function mostrarModal() {
    document.getElementById('modal-buscar').style.display = 'block';
    document.getElementById('descripcion').value = '';
    document.getElementById('resultado-busqueda').innerHTML = '';
    document.getElementById('descripcion').focus();
}

function cerrarModal() {
    document.getElementById('modal-buscar').style.display = 'none';
}

let productosEncontrados = [];
let indiceSeleccionado = -1;

function buscarProductoPorDescripcion() {
    const descripcion = document.getElementById('descripcion').value;
    if (descripcion.length > 0) {
        fetch(`/buscar_producto_descripcion?descripcion=${descripcion}`)
            .then(response => response.json())
            .then(productos => {
                productosEncontrados = productos.slice(0, 15); // Limitar a 15 resultados
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
        });
}

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
