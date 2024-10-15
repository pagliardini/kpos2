const codigoInput = document.getElementById('codigo_producto');
const productosTabla = document.getElementById('productos_tabla');
const totalInput = document.getElementById('total'); // Referencia al input de total
let total = 0; // Variable para almacenar el total

codigoInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        buscarProducto();
    }
});

function buscarProducto() {
    const codigo = codigoInput.value;

    fetch('/buscar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ codigo: codigo }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);  // Mostrar error si el producto no es encontrado
        } else {
            // Crear una nueva fila con los datos del producto, incluyendo la columna "Cantidad"
            const nuevaFila = `
                <tr>
                    <td>${data.codigo1}</td>
                    <td>${data.nombre}</td>
                    <td>${data.costo}</td>
                    <td>${data.stock}</td>
                    <td>1</td>
                </tr>
            `;
            productosTabla.innerHTML += nuevaFila;

            // Sumar el costo al total
            total += parseFloat(data.costo); // Asegúrate de convertir a número
            totalInput.value = total.toFixed(2); // Actualizar el input de total

            // Limpiar el input y poner el foco después de agregar el producto
            codigoInput.value = '';
            codigoInput.focus();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al buscar el producto');
    });
}