#!/bin/bash

ruta=$1
# Activar el entorno virtual
dir="$(dirname "$(realpath "$0")")"
source "$dir/venv_autocommit/bin/activate"

# Ejecutar el script de Python
python3 "$dir/init.py" $ruta

# Desactivar el entorno virtual (opcional)
deactivate
