import config
import gestor as g
def __mostrar_menu_ficheros():
    """Muestra el menú de ficheros."""
    print(g.lista_ficheros())
    print("\nOpciones:")
    print("0. Salir")

def __menu_ficheros():
    """Función principal para el manejo del menú de ficheros."""
    while True:
        __mostrar_menu_ficheros()
        indices_a_eliminar = g.obtener_indices_a_eliminar()
        if indices_a_eliminar == "0":
            return False, config.cambios
        indices = g.procesar_indices(indices_a_eliminar)
        g.eliminar_archivos(indices)
        return True


def menu():
    print("¿Qué deseas hacer?")
    print("1. Elminar ficheros")
    print("2. Elminar ficheros con IA")
    print("3. Generar Commit")
    print("4. Git Commit y Salir")

    print("0. Salir")
    opcion = input("Elige una opción: ")
    if opcion == "0":
        return False
    elif opcion == "1":
        __menu_ficheros()
    elif opcion == "2":
        g.getFicherosAI()
    elif opcion == "3":
        g.getcommit()
        return True
    elif opcion == "4":
        return not g.hacer_commit()
    return True