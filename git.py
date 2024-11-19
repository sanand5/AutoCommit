import os
import subprocess
import config

def git_add(fichero):
    """Añade todos los archivos al índice de Git en el repositorio especificado."""
    subprocess.run(["git", "add", fichero], cwd=config.REPOSITORIO, check=True)

def git_commit(mensaje_commit):
    """Realiza un commit con el mensaje especificado en el repositorio."""
    subprocess.run(mensaje_commit, cwd=config.REPOSITORIO, shell=True, check=True)

def git_diff_exclude(paths=None):
    if paths is None:
        paths = []

    exclude_args = [f":!{path}" for path in paths]

    command = ["git", "diff", "HEAD", "--", "."] + exclude_args

    try:
        with open(config.DIFF_INPUT_FILE, 'w') as diff_file:
            subprocess.run(command, text=True, stdout=diff_file, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar git diff:", e)
