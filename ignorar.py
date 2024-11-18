import os
import config
from pathlib import Path

def buscar_autocommitignore():
    rutas_autocommitignore = []
    
    for root, dirs, files in os.walk(config.REPOSITORIO):
        if '.autocommitignore' in files:
            rutas_autocommitignore.append(os.path.join(root, '.autocommitignore'))
    
    return rutas_autocommitignore

def extraer_rutas_relativas(archivos):
    rutas_relativas = []
    
    for archivo in archivos:
        with open(archivo, 'r') as f:
            for linea in f:
                ruta = linea.strip()
                if ruta and not ruta.startswith("#"):  # Ignorar comentarios
                    # Aquí usamos os.path.join para asegurarnos de que estamos concatenando las rutas correctamente
                    ruta_completa = os.path.join(os.path.dirname(archivo), ruta)
                    # Normalizamos la ruta eliminando redundancias
                    ruta_normalizada = os.path.normpath(ruta_completa)
                    # Si es un archivo o un directorio existente, lo agregamos
                    if os.path.exists(ruta_normalizada):
                        ignore = Path(ruta_normalizada)
                        repo = Path(config.REPOSITORIO)
                        if str(ignore).startswith(str(repo)):
                            relativa = str(ignore.relative_to(repo))
                        rutas_relativas.append(relativa)
    
    return rutas_relativas

def eliminar_archivos_de_cambios(rutas_a_eliminar):
    for ruta in rutas_a_eliminar:
        if ruta in config.cambios:
            del config.cambios[ruta]

def autocommitignore():
    rutas_autocommitignore = buscar_autocommitignore()
    rutas_a_eliminar = extraer_rutas_relativas(rutas_autocommitignore)
    eliminar_archivos_de_cambios(rutas_a_eliminar)
