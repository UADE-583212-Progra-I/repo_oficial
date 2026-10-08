"""
Ojetivo:
1. Repasar listas por comprensión y filter en funciones de búsquedas.
2. Evaluar next cuando el retorno es un solo un elemento (diccionario).
3. Practicar el uso de regex con re.fullmatch para validación de id_tema.
4. Practicar el uso de regex con re.search para búsquedas parciales por 
    nombre y autor.

Actividades:
1. Refactorizar buscar_tema_por_id() de manera de usar lxc o filter con lambda,
    evaluar el uso de next, como sugería la actividad integradora.
2. Evaluar qué sucede si el id_tema ingresado no se puede convertir a int
3. Agregar la función validar_id_tema(id_tema:str).
    de manera que retorne True si id_tema es convertible a int o False si no lo es.
    Desarrollarla primero con métodos de cadena de caracteres 
    y luego con re.fullmatch y regex - hacer pruebas en el Playground.
4. Incorporar la función al Menú principal y probar todo el código.
5. Evaluar primero en el Playground, luego incorporar la función buscar_tema_por_nombre().
6. Evaluar primero en el Playground, luego incorporar la función buscar_tema_por_autor().
7. Cómo se podrían reorganizar las funciones utilizando la estructura de capas,
    presentada en la actividad integradora de la Unidad_8_9?
"""

# ── Importar librerías para regex
import re

# ── Entidad: temas
temas = [
    {"id_tema": 1, "nombre": "Dai Dai", "autor": "Shakira"},
    {"id_tema": 2, "nombre": "Love Yourself", "autor": "BTS"},
    {"id_tema": 3, "nombre": "Waka Waka", "autor": "Shakira"},
    {"id_tema": 4, "nombre": "Fake Love", "autor": "BTS"},
    {"id_tema": 5, "nombre": "Positions", "autor": "Ariana Grande"},
]


def buscar_tema_por_id(id_tema, temas):
    """
    Busca un tema en la lista TEMAS por su id.
    Retorna el diccionario del tema o None si no existe.
    """
    # Validacion
    if not isinstance(id_tema, int):
        print("id_tema debe ser int")
        return None

    for tema in temas:
        if tema["id_tema"] == id_tema:
            return tema
    return None



# Menu principal
id_tema = int(input("ID Tema: "))
print(buscar_tema_por_id(id_tema, temas))


