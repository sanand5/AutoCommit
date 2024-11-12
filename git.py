import os
import subprocess
import config

def git_add(fichero):
    """Añade todos los archivos al índice de Git en el repositorio especificado."""
    subprocess.run(["git", "add", fichero], cwd=config.REPOSITORIO, check=True)

def git_commit(mensaje_commit):
    """Realiza un commit con el mensaje especificado en el repositorio."""
    subprocess.run(mensaje_commit, cwd=config.REPOSITORIO, shell=True, check=True)

def git_diff_head(diff_file_path):
    """Genera el diff y lo escribe en diff.txt en el directorio de salida."""
    try:
        with open(diff_file_path, 'w') as diff_file:
            subprocess.run(["git", "diff", "HEAD"], cwd=config.REPOSITORIO, stdout=diff_file, check=True)
    except subprocess.CalledProcessError:
        print("No se pudieron generar cambios. Asegúrate de que hay cambios para mostrar.")
        exit(1)
