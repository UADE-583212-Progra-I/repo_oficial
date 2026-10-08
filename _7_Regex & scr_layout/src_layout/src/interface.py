import src.utils as utilities

def get_id_tema():
    """Función principal con menú interactivo."""
    id_tema = input("Ingrese el id_tema a buscar: ")
    while not utilities.validar_id_tema(id_tema):
        id_tema = input("ERROR: Ingrese un id_tema válido: ")
    return int(id_tema)