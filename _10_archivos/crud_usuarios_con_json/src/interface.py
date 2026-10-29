import src.utils as utilities

def get_id_usuario():
    id_usuario = input("Ingrese id_usuario: ")
    while not utilities.validar_id_usuario(id_usuario):
        id_usuario = input("ERROR: Ingrese un id_usuario válido: ")
    return int(id_usuario)

def get_nombre():
    nombre = input("Ingrese nombre: ")
    while not utilities.validar_nombre(nombre):
        nombre = input("ERROR: Ingrese un nombre válido: ")
    return nombre

def get_email():
    email = input("Ingrese email: ")
    while not utilities.validar_email(email):
        email = input("ERROR: Ingrese un email válido: ")
    return email

def mostrar_usuarios(usuarios):
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for usuario in usuarios:
        print(usuario)
