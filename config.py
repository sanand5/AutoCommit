import os
import google.generativeai as genai

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))
REPOSITORIO = None
OUTPUT_DIR = os.path.join(DIRECTORIO, 'output')
DIFF_INPUT_FILE = os.path.join(OUTPUT_DIR, 'diff.txt')
DIFF_FORMATED_FILE = os.path.join(OUTPUT_DIR, 'diff_formated.txt')
EXTENSIONES_PERMITIDAS = [
        '.java', '.py', '.js', '.ts', '.c', '.cpp', '.cs', '.rb', '.go', '.php', '.swift', '.html', '.css', '.sql', '.bash', '.sh', 
        '.json', '.yaml', '.yml', '.xml', '.ini', '.ipynb', 
        '.txt', '.md', '.rst', '.log', '.csv', '.tsv', 
        '.config', '.env'
    ]

#genai.configure(api_key=os.environ["API_KEY"])
MODEL = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key="AIzaSyCuRrC6D-DbInVNrIRcU_1EWKrOYdAuBPk")
LIMITE_INTENTOS = 5
PROMPT = """
Esta es la salida de mi `git diff HEAD`. Quiero que generes un único commit que englobe todos los cambios en castellano, utilizando títulos y mensajes apropiados para cada diff. 
- La salida se debe de poder ejectar en la consola
- No debes incluir ningun texto adicional
- La salida debe seguir estrictamente este formato: git commit -m "título descriptivo del commit" -m "mensaje del commit"
- El título puede ser en inglés pero la descripción debe ser en castellano.
Solo debes generar una unica salida
"""

PROMPT_FICHEROS = """
Esta es la lista de los ficheros de mi git diff HEAD
Tu objetivo es darme los indices de los ficheros que creas que no son necesarios para poder eliminarlos de el git diff
- Debes introducirme los indeces separados por espacio.
- Tambien puedes introducir los indices que sean incrementables separados por guiones
Aqui un ejemplo de como es la salida:
1 5 9 11-25
"""
cambios = ""
commit = ""