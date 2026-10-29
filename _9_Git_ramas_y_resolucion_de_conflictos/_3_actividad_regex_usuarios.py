"""
Objetivo:
1. Practicar el uso de regex con re.fullmatch para validación de nombre e email

Actividades:
1. Desarrolla en el Playground la función validar_nombre(),
    luego incorporala al código
2. Desarrolla en el Playground la función validar_email(),
    luego incorporala al código
"""

# ── Importar librerías para regex
import re

# ── Entidad: usuarios
usuarios = []


def validar_nombre(nombre:str):
    patron = r"[a-zA-Z ]+" # completar
    return re.fullmatch(patron, nombre)

def validar_email(email:str):
    patron = r"[\w.+-]+@[\w-]+(\.[A-Za-z0-9-]+)+"
    return re.fullmatch(patron, email)


def crear_usuario(usuarios):
    print("\n--- Crear usuario ---")

    # Solicitar y validar nombre
    nombre = input("Nombre: ").strip()
    while not validar_nombre(nombre):
        print("El nombre solo puede contener letras y espacios.")
        nombre = input("Nombre: ").strip()

    # Solicitar y validar email
    email = input("Email: ").strip()
    while not validar_email(email):
        print("El email ingresado no es válido.")
        email = input("Email: ").strip()

    # Construir el diccionario del usuario
    nuevo_usuario = {
        "nombre": nombre,
        "email": email,
    }

    # Agregar a la lista
    usuarios.append(nuevo_usuario)
    print("Usuario agregado exitosamente!")

crear_usuario(usuarios)