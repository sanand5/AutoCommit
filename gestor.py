import config
import git
import os
import re
import google.api_core.exceptions as api_errors

def print_info():
    print(f"Directorio actual: {config.DIRECTORIO}")
    print(f"Repositorio: {config.REPOSITORIO}")
    print(f"Directorio de salida de el programa: {config.OUTPUT_DIR}")
    print(f"Modelo: {config.MODEL.model_name}")
    print(f"Limite de intentos: {config.LIMITE_INTENTOS}")
    print()

def diffhead():
    git.git_add(".")
    output_dir = crear_directorio_output(config.DIRECTORIO)
    diff_file_path = os.path.join(output_dir, "diff.txt")
    anadir_salto_linea(diff_file_path)
    git.git_diff_head(diff_file_path)
    print(f"Diff generado en: {diff_file_path}")

def crear_directorio_output(directorio_script):
    """Crea el directorio output si no existe."""
    output_dir = os.path.join(directorio_script, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def anadir_salto_linea(diff_file_path):
    """Añade un salto de línea al archivo diff.txt."""
    with open(diff_file_path, 'a') as diff_file:
        diff_file.write("\n")

def anadir_prompt():
    cambios_str = "\n\n".join([f"Ruta: {ruta}\nCambios:\n{diff}" for ruta, diff in config.cambios.items()])
    difftoAI = config.PROMPT + "\n" + cambios_str
    return difftoAI

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
                    if any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                        cambios[ruta_actual] = ''.join(contenido_diff)

                contenido_diff = []  # Reinicia el contenido del diff
                # Usamos expresión regular para obtener las rutas de los archivos (con espacios)
                match = re.match(r'diff --git (a/.+) (b/.+)', linea)
                if match:
                    ruta_actual = match.group(1)  # La ruta del archivo a
            elif ruta_actual:  # Si hay un archivo actual, agrega su contenido
                contenido_diff.append(linea)

        # Guarda el último archivo leído
        if ruta_actual and contenido_diff:
            if any(ruta_actual.endswith(ext) for ext in extensiones_permitidas):
                cambios[ruta_actual] = ''.join(contenido_diff)

    return cambios


def __gemini(msg):
    response = config.MODEL.generate_content(msg)
    return response

def obtener_primera_linea_commit(texto):
    for linea in texto.splitlines():
        if linea.startswith("git commit"):
            return linea
    return None

def getcommit():
    msg = anadir_prompt()
    cont = 0
    continuar = True

    while continuar:
        config.commit = obtener_primera_linea_commit(__gemini(msg).text)
        
        if config.commit != None:
            continuar = False
        else:
            cont += 1
            print(f"La salida de la IA no ha sido la requerida ({cont}/{config.LIMITE_INTENTOS})")
            if cont >= config.LIMITE_INTENTOS:
                return False
    print(config.commit)
    return True


def hacer_commit():
    if config.commit != "":
        if getcommit(): git.git_commit(config.commit)
        else: 
            print("No se ha podido hacer el commit")
            return False
    else: 
        print("No se ha podido hacer el commit")
        return False
    return True

def lista_ficheros():
    rutas = obtener_rutas()  # Suponiendo que esta función devuelve las rutas
    lista_ficheros = "Ficheros:\n"
    for idx, ruta in enumerate(rutas, start=1):
        lista_ficheros += f"\t{idx}. {ruta}\n"
    return lista_ficheros

def getFicherosAI():
    msg = config.PROMPT_FICHEROS + "\n" + lista_ficheros()
    indices_a_eliminar = __gemini(msg).text    
    indices = procesar_indices(indices_a_eliminar)
    eliminar_archivos(indices)




