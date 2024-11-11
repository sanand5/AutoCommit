import os
import subprocess
import config

def __git_add(fichero):
    """Añade todos los archivos al índice de Git."""
    subprocess.run(["git", "add", fichero], check=True)

def __crear_directorio_output(directorio_script):
    """Crea el directorio output si no existe."""
    output_dir = os.path.join(directorio_script, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def __añadir_salto_linea(diff_file_path):
    """Añade un salto de línea al archivo diff.txt."""
    with open(diff_file_path, 'a') as diff_file:
        diff_file.write("\n")

def __git_diff_head(diff_file_path):
    """Genera el diff y lo escribe en diff.txt."""
    try:
        with open(diff_file_path, 'a') as diff_file:
            subprocess.run(["git", "diff", "HEAD"], stdout=diff_file, check=True)
    except subprocess.CalledProcessError:
        print("No se pudieron generar cambios. Asegúrate de que hay cambios para mostrar.")
        exit(1)

def diffhead():
    print(f"Directorio del script: {config.DIRECTORIO}")
    __git_add(".")
    output_dir = __crear_directorio_output(config.DIRECTORIO)
    diff_file_path = os.path.join(output_dir, "diff.txt")
    __añadir_salto_linea(diff_file_path)
    __git_diff_head(diff_file_path)
    print(f"Diff generado en: {diff_file_path}")
