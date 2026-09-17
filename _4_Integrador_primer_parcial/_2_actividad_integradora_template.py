# ============================================================
# Sistema de Recomendación Musical — Parte 1
# Actividad Integradora | Programación I | UADE
# ============================================================
#
# Instrucciones:
#   1. Completá cada función donde dice "# Tu código acá"
#   2. No modifiques los nombres de las funciones ni sus parámetros
#   3. Trabajá en la rama 'develop' y hacé un commit por función
#
# Referencia: _6_sis_rec_part_1_resuelto.py
# ============================================================

import random
from datetime import date


# ============================================================
# DATOS INICIALES
# ============================================================

# ── Entidad: tema (estática, no se modifica durante la ejecución) ─
TEMAS = [
    {"id_tema": 1, "tema": "Dai Dai",          "autor": "Shakira"},
    {"id_tema": 2, "tema": "Dynamite",          "autor": "BTS"},
    {"id_tema": 3, "tema": "DTMF",              "autor": "Bad Bunny"},
    {"id_tema": 4, "tema": "Dont Start Now",    "autor": "Dua Lipa"},
    {"id_tema": 5, "tema": "Positions",         "autor": "Ariana Grande"},
]

# ── Entidad: usuario (se gestiona con CRUD) ──────────────────────
usuarios = []

# ── Relación: rating ─────────────────────────────────────────────
ratings = []


# ============================================================
# SECCIÓN 3 — UTILIDADES GENERALES
# ============================================================


def buscar_tema_por_id(id_tema):
    """
    Busca un tema en la lista TEMAS por su id.
    Retorna el diccionario del tema o None si no existe.
    """
    # Tu código acá
    pass # remover pass, es solo un placeholder 


def buscar_usuario_por_id(id_usuario):
    """
    Busca un usuario en la lista 'usuarios' por su id.
    Retorna el diccionario del usuario o None si no existe.
    """
    # Tu código acá
    pass


# ============================================================
# SECCIÓN 4 — CRUD DE USUARIOS
# ============================================================

# ── Validaciones (Unidad 7 — métodos de string) ──────────────────

def validar_id_usuario(id_usuario):
    """
    Valida que el id_usuario se pueda convertir a int.
    Retorna True si es válido, False si no.

    Métodos útiles: .isdigit()
    """
    # Tu código acá
    pass

def validar_nombre(nombre):
    """
    Valida que el nombre solo contenga letras y espacios, y no esté vacío.
    Retorna True si es válido, False si no.

    Métodos útiles: .strip(), .replace(), .isalpha()
    """
    # Tu código acá
    pass


def validar_email(email):
    """
    Valida que el email contenga '@' y al menos un '.' después del '@'.
    Retorna True si es válido, False si no.

    Métodos útiles: .strip(), 'in', .split(), .find()
    """
    # Tu código acá
    pass


# ── Operaciones CRUD ─────────────────────────────────────────────

def crear_usuario():
    """
    Solicita los datos de un nuevo usuario por teclado.
    Valida nombre, apellido y email antes de agregar.
    Genera el id automáticamente.
    Agrega el usuario a la lista global 'usuarios'.
    """
    print("\n--- Crear usuario ---")

    # Solicitar y validar id_usuario
    id_usuario = input("ID Usuario: ").strip()
    while not validar_id_usuario(id_usuario):
        print("El id_usuario solo puede contener numeros.")
        id_usuario = input("ID Usuario: ").strip()
    id_usuario = int(id_usuario)

    # Solicitar y validar nombre
    nombre = input("Nombre: ").strip()
    while not validar_nombre(nombre):
        print("El nombre solo puede contener letras y espacios.")
        nombre = input("Nombre: ").strip()

    # Tu código acá: solicitar y validar apellido
    apellido = input("")

    # Tu código acá: solicitar y validar email
    email = input("")

    # Construir el diccionario del usuario
    nuevo_usuario = {
        "id_usuario": id_usuario,
        "nombre":     nombre,
        "apellido":   apellido,
        "email":      email,
    }

    # Tu código acá: agregar a la lista 'usuarios'

    print("Usuario agregado exitosamente!")


def buscar_usuario_por_id():
    """
    Solicita un id por teclado y muestra los datos del usuario.
    Si no existe, muestra un mensaje de error.
    """
    print("\n--- Buscar usuario por id ---")

    # Solicitar id_usuario para correr la búsqueda
    id_usuario = int(input("ID del usuario: "))

    # Tu código acá: usar buscar_usuario_por_id()


def ver_usuarios():
    """
    Muestra todos los usuarios de manera paginada.
    Usa slicing para mostrar solo los primeros 5 o 10 registros.
    """
    print("\n--- Primero registros ---")

    if not usuarios:
        print("  No hay usuarios registrados.")
        return


def eliminar_usuario():
    """
    Solicita un id y elimina el usuario de la lista.
    Usa .pop() o .remove() sobre la lista (Unidad 7 — métodos de lista).
    Si el usuario no existe, muestra un mensaje de error.
    NOTA: Deberíamos eliminar todos los ratings asociados a ese usuario,
    pero no lo haremos.
    """
    print("\n--- Eliminar usuario ---")
    id_usuario = int(input("ID del usuario a eliminar: "))

    usuario = buscar_usuario_por_id(id_usuario)
    if not usuario:
        print(f"No se encontró ningún usuario con id {id_usuario}.")
        return

    # Tu código acá: eliminar el usuario de la lista 'usuarios'
    # Podés usar .remove() pasando el objeto, o .pop() con el índice


    print(f"Usuario eliminado correctamente.")


# ============================================================
# SECCIÓN 5 — GESTIÓN DE RATINGS
# ============================================================

def registrar_rating():
    """
    Solicita id_usuario, id_tema y valor del rating (1-5).

    Mejoras futuras:
    1. si el usuario ya calificó ese tema, actualiza el rating existente.
       Si no, crea un rating nuevo.
    2. Validar que el usuario y el tema existan.
    3. Usa la fecha del día de hoy con date.today().
    """
    print("\n--- Registrar rating ---")
    id_rating = int(input("ID del rating: "))
    id_usuario = int(input("ID del usuario: "))
    id_tema    = int(input("ID del tema: "))
    valor_rating = int(input("Rating (1 a 5): "))
    fecha = input("")

    nuevo_rating = {
        "id_rating":  id_rating,
        "id_usuario": id_usuario,
        "id_tema":    id_tema,
        "rating":     valor_rating,
        "fecha":      fecha,
    }
    ratings.append(nuevo_rating)
    print(f"Rating registrado correctamente.")


def leer_ratings():
    """
    Muestra todos los ratings con nombre de usuario y nombre de tema.
    
    Mejoras futuras: JOIN manual entre las tres listas
    """
    print("\n--- Ratings registrados ---")


# ============================================================
# SECCIÓN 6 — MATRIZ DE RATINGS
# ============================================================

def construir_matriz_ratings():
    """
    Construye la matriz de doble entrada a partir de las listas globales.

    Retorna una lista de listas (matriz) donde:
        - matriz[i][j] = rating del usuario i al tema j
        - 0 si el usuario no calificó ese tema

    Los usuarios y temas se ordenan por su id para mantener
    consistencia con la función mostrar_matriz.
    """
    if not usuarios:
        return []
 
    # Índice (id_usuario, id_tema) → rating para búsqueda en O(1)
    indice = {}
    for r in ratings:
        clave = (r["id_usuario"], r["id_tema"])
        indice[clave] = r["rating"]
 
    # Ordenar por id para consistencia
    usuarios_ord = sorted(usuarios, key=lambda u: u["id_usuario"])
 
    # Construir la matriz fila por fila
    matriz = []
    for u in usuarios_ord:
        fila = []
        for t in TEMAS:
            clave = (u["id_usuario"], t["id_tema"])
            fila.append(indice.get(clave, 0))
        matriz.append(fila)
 
    return matriz



def mostrar_matriz_ratings():
    """Muestra la matriz de ratings."""

    matriz = construir_matriz_ratings()

    if not matriz:
        print("No hay datos suficientes.")
        return

    # Encabezado
    print("Usuario", end=" ")

    for tema in TEMAS:
        print(tema["tema"], end=" ")

    print()

    # Matriz
    for i, fila in enumerate(matriz):
        print(usuarios[i]["nombre"], end=" ")

        for rating in fila:
            print(rating, end=" ")

        print()


# ============================================================
# SECCIÓN 7 — MENÚ INTERACTIVO
# ============================================================

def menu_usuarios():
    """Submenú de gestión de usuarios."""
    while True:
        print("\n  --- Gestión de Usuarios ---")
        print("  1. Crear usuario")
        print("  2. Ver usuario por ID")
        print("  3. Ver todos los usuarios (primeros registros)")
        print("  4. Eliminar usuario")
        print("  0. Volver")

        opcion = input("\n  Opción: ").strip()
        if   opcion == "1": crear_usuario()
        elif opcion == "2": buscar_usuario_por_id()
        elif opcion == "3": ver_usuarios()
        elif opcion == "4": eliminar_usuario()
        elif opcion == "0": break
        else: print("Opción inválida.")


def menu_ratings():
    """Submenú de gestión de ratings."""
    while True:
        print("\n  --- Gestión de Ratings ---")
        print("  1. Registrar rating")
        print("  2. Ver todos los ratings")
        print("  0. Volver")

        opcion = input("\n  Opción: ").strip()
        if   opcion == "1": registrar_rating()
        elif opcion == "2": leer_ratings()
        elif opcion == "0": break
        else: print("Opción inválida.")


def main():
    """Función principal con menú interactivo."""
    while True:
        print("\n" + "=" * 45)
        print("   Sistema de Recomendación Musical")
        print("=" * 45)
        print("1. Ver temas disponibles")
        print("2. Gestionar usuarios")
        print("3. Gestionar ratings")
        print("4. Ver matriz de ratings")
        print("0. Salir")

        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            print("\n--- Temas disponibles ---")
            for t in TEMAS:
                print(f"  [{t['id_tema']}] {t['tema']} — {t['autor']}")

        elif opcion == "2":
            menu_usuarios()

        elif opcion == "3":
            menu_ratings()

        elif opcion == "4":
            mostrar_matriz_ratings()

        elif opcion == "0":
            print("\n¡Hasta luego! 🎵")
            break

        else:
            print("Opción inválida. Ingresá un número del menú.")


# ============================================================
if __name__ == "__main__":
    main()
