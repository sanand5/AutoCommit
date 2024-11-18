import config
import git
from file_utils import crear_directorio_output, anadir_salto_linea, leer_diff, guardar
import google.api_core.exceptions as api_errors
import os


def print_info():
    """Muestra información relevante de la configuración."""
    print(f"Directorio actual: {config.DIRECTORIO}")
    print(f"Repositorio: {config.REPOSITORIO}")
    print(f"Directorio de salida del programa: {config.OUTPUT_DIR}")
    print(f"Modelo: {config.MODEL.model_name}")
    print(f"Límite de intentos: {config.LIMITE_INTENTOS}")
    print()

def diffhead():
    """Genera un diff del repositorio y lo guarda en un archivo."""
    git.git_add(".")
    output_dir = crear_directorio_output(config.DIRECTORIO)
    diff_file_path = os.path.join(output_dir, "diff.txt")
    anadir_salto_linea(diff_file_path)
    git.git_diff_head(diff_file_path)
    print(f"Diff generado en: {diff_file_path}")

def anadir_prompt():
    """Genera el mensaje con los cambios a enviar a la IA."""
    cambios_str = "\n\n".join([f"Ruta: {ruta}\nCambios:\n{diff}" for ruta, diff in config.cambios.items()])
    return config.PROMPT + "\n" + cambios_str

def obtener_rutas():
    """Obtiene las rutas de los cambios registrados."""
    return list(config.cambios.keys())

def obtener_indices_a_eliminar():
    """Solicita los índices de archivos a eliminar."""
    return input("Introduce los ficheros a eliminar (separados por espacio o un rango como 7-10): ")

def procesar_indices(indices_a_eliminar):
    """Procesa los índices ingresados para determinar los archivos a eliminar."""
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
    """Elimina los archivos según los índices proporcionados."""
    rutas = obtener_rutas()
    for idx in sorted(indices, reverse=True):
        if 0 <= idx < len(rutas):
            config.cambios.pop(rutas[idx], None)

def __gemini(msg):
    """Genera el contenido usando la IA configurada."""
    return config.MODEL.generate_content(msg)

def obtener_primera_linea_commit(texto):
    """Obtiene la primera línea de commit de un mensaje."""
    for linea in texto.splitlines():
        if linea.startswith("git commit"):
            return linea
    return None

def getcommit():
    """Obtiene un mensaje de commit generado por la IA."""
    msg = anadir_prompt()
    cont = 0
    continuar = True

    while continuar:
        config.commit = obtener_primera_linea_commit(__gemini(msg).text)
        
        if config.commit:
            continuar = False
        else:
            cont += 1
            print(f"La salida de la IA no ha sido la requerida ({cont}/{config.LIMITE_INTENTOS})")
            if cont >= config.LIMITE_INTENTOS:
                return False
    print(config.commit)
    return True

def hacer_commit():
    """Realiza el commit si el mensaje es válido."""
    if config.commit:
        if getcommit():
            git.git_commit(config.commit)
        else:
            print("No se ha podido hacer el commit")
            return False
    else:
        print("No se ha podido hacer el commit")
        return False
    return True

def lista_ficheros():
    """Genera una lista de archivos con sus índices."""
    rutas = obtener_rutas()
    lista_ficheros = "Ficheros:\n"
    for idx, ruta in enumerate(rutas, start=1):
        lista_ficheros += f"\t{idx}. {ruta}\n"
    return lista_ficheros

def getFicherosAI():
    """Obtiene los ficheros a eliminar mediante la IA."""
    msg = config.PROMPT_FICHEROS + "\n" + lista_ficheros()
    indices_a_eliminar = __gemini(msg).text    
    indices = procesar_indices(indices_a_eliminar)
    eliminar_archivos(indices)
