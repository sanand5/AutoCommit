import config
import gestor as g
import menu as m
import git as git

def autocommit():
    g.diffhead()
    archivo_diff = config.DIFF_INPUT_FILE  # Archivo con los cambios en formato diff
    config.cambios = g.leer_diff(archivo_diff, config.EXTENSIONES_PERMITIDAS)
    seguir = True
    while seguir:
        tokens, difftoAI = g.tokenizar_cambios()
        seguir = m.menu()
    tokens, difftoAI = g.tokenizar_cambios()
    g.guardar(difftoAI)
    return difftoAI
