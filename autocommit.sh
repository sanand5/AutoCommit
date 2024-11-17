#!/bin/bash

ruta=$1
# Activar el entorno virtual
source ./venv_autocommit/bin/activate

# Ejecutar el script de Python
python3 ./init.py $ruta

# Desactivar el entorno virtual (opcional)
deactivate
