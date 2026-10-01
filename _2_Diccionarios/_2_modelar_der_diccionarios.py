# ============================================================
# ESTRUCTURAS DE DATOS PARA EXHIBICION DE PINTURAS EN GALERIAS
# Entidades: galeria · pintura · artista
# Programación I | UADE
# ============================================================
#
# En esta actividad vamos a representar las entidades del
# sistema de recomendación usando listas y diccionarios.
#
#   galeria ──(1:N)── pintura ──(N:1)── artista
#
# ============================================================


# ============================================================
# REPRESENTACIÓN CON DICCIONARIOS
# ============================================================

# Declaramos una constante
INDICE = ""

# ── Entidad: artista (ya construida para referencia) ─────────
# Cada registro es un diccionario: clave = nombre del campo
artista_1 = {"id_artista": 1, "nombre_artista": "Branksy", "nacionalidad": "Inglaterra"}
artista_2 = {"id_artista": 2, "nombre_artista": "Kusama", "nacionalidad": "Japon"}
artista_3 = {"id_artista": 3, "nombre_artista": "Koons", "nacionalidad": "EEUU"}
artista_4 = {"id_artista": 4, "nombre_artista": "Hirst", "nacionalidad": "Inglaterra"}
artista_5 = {"id_artista": 5, "nombre_artista": "Murakami", "nacionalidad": "Japon"}

# La "tabla" de artistas: una lista de diccionarios
artistas = [artista_1, artista_2, artista_3, artista_4, artista_5]


# ── Actividad 1 — Trabajamos con la entidad galeria ──────────────────

# Paso 1: Construí las primeras dos galerias como diccionarios.
# Usá como referencia los diccionarios de artista de arriba.
#
# Campos de la galeria:
#   id_galeria | nombre_galeria | ciudad | pais
#
# Datos:
#   1 | MOMA | New York | EEUU
#   2 | Guggenheim | New York | EEUU


galeria_1 = {"id_galeria": 1, "nombre_galeria": "MOMA", "ciudad": "New York", "pais": "EEUU"}
galeria_2 = {"id_galeria": 2, "nombre_galeria": "Guggenheim", "ciudad": "New York", "pais": "EEUU"}

# Paso 2: Armá la lista de galeroas con los dos registros creados arriba.
galerias = [galeria_1, galeria_2]
# galerias.pop(0) #eliminar galeria_1

# ********** FUNCIONES AUXILIARES ***************
def mostrar_artistas(artistas):
    for registro in artistas:
        print(registro)


# Paso 3:
# completa la función que muestra las galerías en terminal
def mostrar_galerias(galerias):
    for regitro in galerias:
        print(regitro)


# Paso 4:
# Completa la función ingresar_galeria() para ingresar por terminal los campos de la galeria
# Con esos datos, arma un diccionario (registro) y agregalo a la lista galerias usando append()

# Datos pendientes a ingresar:
# 3 | Louvre | Paris | Francia
# 4 | Orsay | Paris | Francia
# 5 | Brera | Milan | Italia

# Utilities 
def validar_id_galeria(id_galeria:str):
    """
    Valida que el id_galeria se pueda convertir a int.
    Retorna True si es válido, False si no.
    """
    return id_galeria.isdigit()

def validar_nombre_galeria(nombre:str):
    """
    Return False si nombre es igual ""
    Return True si nombre es distinto de ""

    """
    # Completar 
    # if nombre: # si nombre es "" retorna False
    # if nombre == "": 
    # if len(nombre) == 0:
    #     return False
    # else:
    #     return True 
    return len(nombre)!=0

# Funciones de lectura por terminal
def leer_id_galeria():
    """
    Lee por terminal el id de la galeria
    retorna el id_galeria validado
    """
    id_galeria = input("ID Galeria: ").strip()
    while not validar_id_galeria(id_galeria):
        print("El ID de la galeria solo puede contener numeros.")
        id_galeria = input("ID Galeria: ").strip()

    return int(id_galeria)

def leer_nombre():
    nombre = input("Nombre de la galeria: ").strip()
    while not validar_nombre_galeria(nombre):
        print("El nombre de la galeria no puede estar vacia.")
        nombre = input("Nombre de la galeria: ").strip()

    return nombre

def ingresar_galeria():
    """
    Crea un diccionario - registro de una galería
    Retorna un diccionario con los campos de la entidad
    """
    id = leer_id_galeria()
    nombre = leer_nombre()
    ciudad = input("Ingrese la ciudad: ")
    pais = input("Ingrese el pais: ")

    galeria = {
        "id_galeria": id,
        "nombre_galeria": nombre,
        "ciudad": ciudad,
        "pais": pais,
    }

    return galeria


# Paso : generá un Loop en la función main que llame a la función
# # ingresar_galeria() - se sugiere que el usuario indique fin de carga


def buscar_galeria_id(id_galeria:int, galerias:list):
    """
    DocString
    parametro: id_galeria:int, galerias:list
    return: lista de diccionarios (longitud 0 si no hay match o 1 si hay match)
    """
    lista_encontrados = []
    for galeria in galerias:
        if galeria["id_galeria"] == id_galeria:
            lista_encontrados.append(galeria)
            break
    return lista_encontrados


def buscar_galeria_pais(pais:str, galerias:list):
    """
    DocString
    parametro: pais:str, galerias:list
    return: lista de diccionarios
    """
    lista_encontrados = []
    for galeria in galerias:
        if galeria["pais"].strip().lower() == pais.strip().lower():
            lista_encontrados.append(galeria)
    return lista_encontrados


def eliminar_galeria_id(id_galeria:int, galerias:list):
    """
    DocString
    parametro: id_galeria:str, galerias:list
    return: Ok True - Mal False / diccionarop
    """
    # opcion 1
    for galeria in galerias: 
        if galeria["id_galeria"] == id_galeria:
            galerias.remove(galeria) # opcion 1
            return True # -> break
    return False 

    # opcion 2
    # for indice, galeria in enumerate(galerias): # enumerate -> (indice, valor)
    #     if galeria["id_galeria"] == id_galeria:
    #         galerias.pop(indice) 


# ********** FUNCION PRINCIPAL ***************
def main():
    print("Artistas ")
    mostrar_artistas(artistas)

    print("\nGalerias")
    mostrar_galerias(galerias)
    # Create
    galeria = ingresar_galeria()
    galerias.append(galeria)

    # Buscar
    id_galeria = input("Ingrese id a buscar")
    lista_encontrados = buscar_galeria_id(id_galeria)
    if len(lista_encontrados)!=0:
        print(lista_encontrados[0])
    else:
        print("No encontrado")
    
    # Eliminar
    id_galeria = input("Ingrese id a eliminar")
    respuesta = eliminar_galeria_id(id_galeria)
    if respuesta == True:
        print("Eliminado Exitosamente")
    else:
        print("Error al eliminar!")


# Llamada a la función principal
main()

# Paso 5:
# Genera la función buscar_galeria_pais() que recibe como argumento un país
# y retorna una lista con todos los campos de la entidad galeria de ese país

# Paso 6:
# Genera la función eliminar_galeria_id() que recibe el id_galeria
# busca ese id entre los registros de la entidad galería, y si lo encuentra,
# lo elimina. Caso contrario indica al usuario que ese id no existe.

# Paso 7:
# Genera en la función main, un menú para la entidad galeria,
# con las opciones:
# 1. Crear nueva galeria
# 2. Buscar galeria por país
# 3. Eliminar galeria po id

# Asi tendrás casi listo el CRUD para una entidad de tu proyecto!
