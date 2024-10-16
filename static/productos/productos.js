// Evita el envío del formulario al presionar 'Enter' en el campo de código
document.addEventListener('DOMContentLoaded', function() {
    const codigoField = document.getElementById('codigoInput');
    codigoField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.querySelector('input[type="text"][placeholder="Escribe para buscar"]');
    const tbody = document.querySelector('tbody');

    // Función para cargar productos en la tabla
    function cargarProductos(productos) {
        tbody.innerHTML = '';  // Limpiar la tabla
        productos.forEach((producto, index) => {
            const row = document.createElement('tr');

            // Aplicar colores de fila alternos (opcional)
            if (index % 2 === 0) {
                row.classList.add('bg-gray-100');
            } else {
                row.classList.add('bg-white');
            }

            // Crear HTML para la fila de la tabla
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${producto.codigo1 || ''}</td>
                <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${producto.nombre || ''}</td>
                <td>$${producto.costo || 0}</td>
                <td>$${producto.precio || 0}</td>
                <td>${producto.stock || 0}</td>
                <td>
                    <a href="/productos/editar/${producto.id}" class="text-blue-500 hover:underline">Editar</a>
                    <form action="/productos/eliminar/${producto.id}" method='POST' style='display:inline;'>
                        <button type='submit' class='text-red-500 hover:underline ml-4'>Eliminar</button>
                    </form>
                </td>
            `;
            tbody.appendChild(row); // Agregar la nueva fila
        });
    }

    // Cargar los primeros 50 productos al iniciar
    fetch(`/productos?limit=50`)
        .then(response => response.json())
        .then(data => {
            cargarProductos(data.productos);
        });

    // Evita el envío del formulario al presionar 'Enter' en el campo de código
    const codigoField = document.getElementById('codigoInput');
    codigoField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    // Función para buscar productos cuando se escribe en el campo de búsqueda
    inputBusqueda.addEventListener('input', function() {
        const query = inputBusqueda.value.trim();

        if (query.length > 0) {
            fetch(`/productos/buscar?q=${query}`)
                .then(response => response.json())
                .then(productosFiltrados => {
                    cargarProductos(productosFiltrados);
                });
        } else {
            // Si el campo de búsqueda está vacío, cargar los primeros 50 productos de nuevo
            fetch(`/productos?limit=50`)
                .then(response => response.json())
                .then(data => {
                    cargarProductos(data.productos);
                });
        }
    });
});