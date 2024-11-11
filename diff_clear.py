import config
import tiktoken
import os
import getcommit as gc


def __leer_diff(archivo_diff, extensiones_permitidas):
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

def __tokenizar_cambios():
    # Convierte el diccionario de cambios a una sola cadena de texto
    cambios_str = "\n\n".join([f"Ruta: {ruta}\nCambios:\n{diff}" for ruta, diff in config.cambios.items()])
    difftogpt = config.PROMPT + "\n" + cambios_str
    # Tokeniza usando tiktoken
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(difftogpt)
    return tokens, cambios_str, difftogpt

def __menu_ficheros():
    print("Ficheros:")
    rutas = list(config.cambios.keys())
    for idx, ruta in enumerate(rutas, start=1):
        print(f"{idx}. {ruta}")

    # Opción de salir
    print("\nOpciones:")
    print("0. Salir")

    # Eliminar archivos por índice o por rango
    indices_a_eliminar = input("Introduce los ficheros a eliminar (separados por espacio o un rango como 7-10): ")

    if indices_a_eliminar == "0":
        return False, config.cambios  # Salir del menú

    # Procesar eliminación por rangos
    indices = set()
    for parte in indices_a_eliminar.split():
        if '-' in parte:
            start, end = parte.split('-')
            try:
                start, end = int(start), int(end)
                indices.update(range(start - 1, end))  # Restar 1 para índice 0 basado
            except ValueError:
                print("Rango no válido.")
        elif parte.isdigit():
            indices.add(int(parte) - 1)  # Restar 1 para índice 0 basado

    # Elimina los archivos seleccionados
    rutas = list(config.cambios.keys())
    for idx in sorted(indices, reverse=True):
        if 0 <= idx < len(rutas):
            config.cambios.pop(rutas[idx], None)
    
    return True

def __menu():
    print("¿Qué deseas hacer?")
    print("1. Elminar ficheros")
    print("2. Dividir en diferentes ficheros y salir")
    opcion = input("Elige una opción: ")
    if opcion == "1":
        __menu_ficheros()
        return True
    elif opcion == "2":
        return False

def __dividir_y_guardar(cambios_str, tokens):
    # Si los tokens son mayores que el límite, divide en varias partes
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    total_tokens = len(tokens)

    if total_tokens > config.LIMITE_TOKENS:
        num_ficheros = (total_tokens // config.LIMITE_TOKENS) + 1
        tokens_por_fichero = total_tokens // num_ficheros

        for i in range(num_ficheros):
            start = i * tokens_por_fichero
            end = start + tokens_por_fichero
            parte_tokens = tokens[start:end]
            parte_texto = enc.decode(parte_tokens)
            with open(os.path.join(config.OUTPUT_DIR, f"cambios_parte_{i + 1}.txt"), "w") as f:
                f.write(parte_texto)
    else:
        with open(config.DIFF_FORMATED_FILE, "w") as f:
            f.write(cambios_str)
    
def diff_clear():
    archivo_diff = config.DIFF_INPUT_FILE  # Archivo con los cambios en formato diff
    config.cambios = __leer_diff(archivo_diff, config.EXTENSIONES_PERMITIDAS)
    seguir = True
    while seguir:
        tokens, cambios_str, difftogpt = __tokenizar_cambios()
        if len(tokens) > config.LIMITE_TOKENS:
            print(f"Has superado el límite de tokens. {len(tokens)}/{config.LIMITE_TOKENS}")
        seguir = __menu()
    tokens, cambios_str, difftogpt = __tokenizar_cambios()
    __dividir_y_guardar(difftogpt, tokens)
    commit = gc.gemini(difftogpt).text
    print(commit)
