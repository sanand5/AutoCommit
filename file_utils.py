import os
import re
import config

def crear_directorio_output(directorio_script):
    """Crea el directorio output si no existe."""
    output_dir = os.path.join(directorio_script, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def anadir_salto_linea(diff_file_path):
    """Añade un salto de línea al archivo diff.txt."""
    with open(diff_file_path, 'a') as diff_file:
        diff_file.write("\n")

def leer_diff(archivo_diff, extensiones_permitidas):
    """Lee un archivo diff y filtra por extensiones permitidas."""
    cambios = {}
    ruta_actual = None
    contenido_diff = []

    with open(archivo_diff, 'r') as f:
        for linea in f:
            if linea.startswith('diff --git'):
                if ruta_actual and contenido_diff:
                    if any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                        cambios[ruta_actual] = ''.join(contenido_diff)

                contenido_diff = []  # Reinicia el contenido del diff
                match = re.match(r'diff --git (a/.+) (b/.+)', linea)
                if match:
                    ruta_actual = match.group(1)  # La ruta del archivo a
            elif ruta_actual:
                contenido_diff.append(linea)

        if ruta_actual and contenido_diff:
            if any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                cambios[ruta_actual] = ''.join(contenido_diff)

    return cambios

def guardar(cambios_str):
    """Guarda los cambios formateados en un archivo."""
    with open(config.DIFF_FORMATED_FILE, "w") as f:
        f.write(cambios_str)
