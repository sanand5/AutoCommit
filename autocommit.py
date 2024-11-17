import config
import gestor as g
import menu as m
import git as git
import sys

def autocommit():
    config.REPOSITORIO = sys.argv[1]
    g.print_info()
    g.diffhead()
    config.cambios = g.leer_diff(config.DIFF_INPUT_FILE, config.EXTENSIONES_PERMITIDAS)
    seguir = True
    while seguir:
        difftoAI = g.anadir_prompt()
        seguir = m.menu()
    difftoAI = g.anadir_prompt()
    g.guardar(difftoAI)
    return difftoAI
