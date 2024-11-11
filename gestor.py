import config
import tiktoken
import git
import os

def diffhead():
    print(f"Directorio del script: {config.DIRECTORIO}")
    git.git_add(".")
    output_dir = crear_directorio_output(config.DIRECTORIO)
    diff_file_path = os.path.join(output_dir, "diff.txt")
    añadir_salto_linea(diff_file_path)
    git.git_diff_head(diff_file_path)
    print(f"Diff generado en: {diff_file_path}")

def crear_directorio_output(directorio_script):
    """Crea el directorio output si no existe."""
    output_dir = os.path.join(directorio_script, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def añadir_salto_linea(diff_file_path):
    """Añade un salto de línea al archivo diff.txt."""
    with open(diff_file_path, 'a') as diff_file:
        diff_file.write("\n")

def tokenizar_cambios():
    cambios_str = "\n\n".join([f"Ruta: {ruta}\nCambios:\n{diff}" for ruta, diff in config.cambios.items()])
    difftoAI = config.PROMPT + "\n" + cambios_str
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(difftoAI)
    return tokens, difftoAI

def guardar(cambios_str):
    with open(config.DIFF_FORMATED_FILE, "w") as f:
            f.write(cambios_str)

def obtener_rutas():
    return list(config.cambios.keys())

def obtener_indices_a_eliminar():
    return input("Introduce los ficheros a eliminar (separados por espacio o un rango como 7-10): ")

def procesar_indices(indices_a_eliminar):
    indices = set()
    for parte in indices_a_eliminar.split():
        if '-' in parte:
            try:
                start, end = map(int, parte.split('-'))
                indices.update(range(start - 1, end))  # Restar 1 para índice basado en 0
            except ValueError:
                print("Rango no válido.")
        elif parte.isdigit():
            indices.add(int(parte) - 1)  # Restar 1 para índice basado en 0
    return indices

def eliminar_archivos(indices):
    rutas = obtener_rutas()
    for idx in sorted(indices, reverse=True):
        if 0 <= idx < len(rutas):
            config.cambios.pop(rutas[idx], None)

def leer_diff(archivo_diff, extensiones_permitidas):
    cambios = {}
    ruta_actual = None
    contenido_diff = []

    with open(archivo_diff, 'r') as f:
        for linea in f:
            # Verifica si la línea indica el inicio de un nuevo archivo
            if linea.startswith('diff --git'):
                if ruta_actual and contenido_diff:
                    # Filtrar cambios según la extensión del archivo
                    if not any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                        cambios[ruta_actual] = "Modificaciones de este fichero"
                    else:
                        cambios[ruta_actual] = ''.join(contenido_diff)

                contenido_diff = []  # Reinicia el contenido del diff
                # Extrae la ruta del nuevo archivo
                partes = linea.split()
                ruta_actual = partes[2] if len(partes) > 2 else None
            elif ruta_actual:  # Si hay un archivo actual, agrega su contenido
                contenido_diff.append(linea)

        # Guarda el último archivo leído
        if ruta_actual and contenido_diff:
            if not any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                cambios[ruta_actual] = "Modificaciones de este fichero"
            else:
                cambios[ruta_actual] = ''.join(contenido_diff)

    return cambios


def __gemini(msg):
    response = config.MODEL.generate_content(msg)
    return response

def getcommit():
    tokens, msg = tokenizar_cambios()
    config.commit = __gemini(msg).text[1:-1]
    return config.commit

def hacer_commit():
    git.git_commit(config.commit.replace("git commit -m ", ""))