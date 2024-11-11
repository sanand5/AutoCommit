import os
import subprocess
import config

def git_add(fichero):
    """Añade todos los archivos al índice de Git."""
    subprocess.run(["git", "add", fichero], check=True)

def git_commit(mensaje_commit):
    """Realiza un commit con el mensaje especificado."""
    subprocess.run(["git", "commit", "-m", mensaje_commit], check=True)

def git_diff_head(diff_file_path):
    """Genera el diff y lo escribe en diff.txt."""
    try:
        with open(diff_file_path, 'a') as diff_file:
            subprocess.run(["git", "diff", "HEAD"], stdout=diff_file, check=True)
    except subprocess.CalledProcessError:
        print("No se pudieron generar cambios. Asegúrate de que hay cambios para mostrar.")
        exit(1)



