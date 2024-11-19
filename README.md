# AutoCommit - Generación Automática de Commits
## Descripción
AutoCommit es una herramienta que simplifica la creación de commits en Git utilizando la API de Google Generative AI. Facilita la generación automática de mensajes de commit basados en los cambios detectados en el repositorio y permite filtrar archivos de forma manual o automatizada usando inteligencia artificial.

## Funcionalidades
- Generación automática de mensajes de commit usando un modelo de IA.
- Filtrado de archivos en el git diff para excluir los irrelevantes.
- Posibilidad de ignorar rutas específicas mediante un fichero `.autocommit`.
- Integración con Git, incluyendo adición (git add), creación de diffs (git diff) y commits (git commit).
- Interfaz de línea de comandos para una fácil interacción.
- Compatibilidad con diferentes tipos de archivos para análisis de diffs.

## Instalación
### Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd AutoCommit
```
### Instalar dependencias:
```bash
python3 -m venv venv_autocommit
source venv_autocommit/bin/activate
pip install -r requirements.txt
```
### Configurar la API Key de Google Generative AI:
Asegúrate de tener configurada la variable de entorno `API_KEY` con tu clave de API:
```bash
export API_KEY="tu_api_key"
```

## Uso
### Comando principal
El script de shell `autocommit.sh` permite ejecutar el proceso completo de generación de commits:
```bash
bash autocommit.sh <ruta_del_repositorio>
```
## Ignorar rutas con el fichero .autocommit
Si se incluye un fichero .autocommit en el directorio raíz del repositorio, las rutas especificadas en su interior serán ignoradas al momento de generar el commit. Estas rutas pueden ser absolutas o relativas al repositorio.

### Ejemplo de contenido de .autocommit:
```
/ruta/absoluta/a/ignorar
directorio/relativo/a/ignorar
archivo_relativo.txt
```
## Menú de opciones
Durante la ejecución, se te presentará un menú con las siguientes opciones:

1. **Eliminar ficheros manualmente**: Permite seleccionar archivos del git diff para eliminar manualmente.
2. **Eliminar ficheros con IA**: Utiliza IA para sugerir archivos a eliminar del git diff.
3. **Generar Commit**: Genera un mensaje de commit utilizando IA.
4. **Git Commit y Salir**: Crea el commit con el mensaje generado y termina el proceso.

## Requisitos
- Python 3.8 o superior.
- Acceso a la API de Google Generative AI.
- Git instalado y configurado.

## Contribuir
1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m "Agregar nueva funcionalidad"`).
4. Envía tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Crea un Pull Request.
