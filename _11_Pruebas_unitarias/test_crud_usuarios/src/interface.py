import src.utils as utilities
from tabulate import tabulate

def get_id_usuario():
    """Lee y valida por terminal el campo id_usuario
    Retorna el id_usuario casteado a int"""
    id_usuario = input("Ingrese id_usuario: ")
    while not utilities.validar_id_usuario(id_usuario):
            id_usuario = input("ERROR: Ingrese un id_usuario válido: ")
    return int(id_usuario)

def get_nombre():
    """Lee y valida por terminal el campo nombre y lo retorna"""
    nombre = input("Ingrese nombre: ")
    while not utilities.validar_nombre(nombre):
        nombre = input("ERROR: Ingrese un nombre válido: ")
    return nombre

def get_email():
    """Lee y valida por terminal el campo email y lo retorna"""
    email = input("Ingrese email: ")
    while not utilities.validar_email(email):
        email = input("ERROR: Ingrese un email válido: ")
    return email

def get_nuevo_usuario():
    """Arma y retorna un diccionario con los campos nombre e email"""
    nuevo_usuario = {
        "nombre": get_nombre(),
        "email": get_email()
    }
    return nuevo_usuario

def mostrar_usuarios(usuarios):
    """Recibe una lista de diccionario y muestra los registros usando Tabulate
    Si la lista esta vacía, imprime un mensaje"""
    if not usuarios:
        mostrar_warning("No hay usuarios registrados.")
        return
    print(tabulate(usuarios, headers="keys", tablefmt="grid"))


def mostrar_mensaje(mensaje):
    """Muestra de forma personaliada un info"""
    print(mensaje)

def mostrar_warning(mensaje):
    """Muestra de forma personaliada un warning"""
    print(f"WARNING: {mensaje}")

def mostrar_error(mensaje):
    """Muestra de forma personaliada un error"""
    print(f"ERROR: {mensaje}")