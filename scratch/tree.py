import os


def listar_archivos(directorio):
    for carpeta, subcarpetas, archivos in os.walk(directorio):
        # Excluye las carpetas __pycache__ y venv
        subcarpetas[:] = [s for s in subcarpetas if s not in ['__pycache__', 'venv', '.git', '.idea', 'scratch']]

        nivel = carpeta.replace(directorio, '').count(os.sep)
        indentacion = ' ' * 4 * (nivel)
        print(f"{indentacion}{os.path.basename(carpeta)}/")

        for archivo in archivos:
            print(f"{indentacion}    {archivo}")


# Cambia '.' por la ruta de tu proyecto si es necesario
listar_archivos('..')