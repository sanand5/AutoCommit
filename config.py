import os
import google.generativeai as genai

LIMITE_TOKENS = 4096
PROMPT = """En esta conversación, te proporcionaré la salida de mi `git diff HEAD`. Quiero que me ayudes a crear un único commit que englobe todos los cambios, utilizando títulos y mensajes apropiados para cada diff, siguiendo los consejos anteriores. La salida debe seguir estrictamente esta plantilla:
`git commit -m "título descriptivo del commit" -m "mensaje del commit"`
El título puede ser en inglés pero la descripción debe ser en castellano.
Por favor, no incluyas ningún texto adicional."""
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(DIRECTORIO, 'output')
DIFF_INPUT_FILE = os.path.join(OUTPUT_DIR, 'diff.txt')
DIFF_FORMATED_FILE = os.path.join(OUTPUT_DIR, 'diff_formated.txt')
EXTENSIONES_PERMITIDAS = [
        '.java', '.py', '.js', '.ts', '.c', '.cpp', '.cs', '.rb', '.go', '.php', '.swift', '.html', '.css', '.sql', '.bash', '.sh', 
        '.json', '.yaml', '.yml', '.xml', '.ini', 
        '.txt', '.md', '.rst', '.log', '.csv', '.tsv', 
        '.config', '.env'
    ]
cambios = ""

#genai.configure(api_key=os.environ["API_KEY"])
MODEL = genai.GenerativeModel("gemini-1.5-flash")