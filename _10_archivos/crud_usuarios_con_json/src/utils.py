import re

def validar_id_usuario(id_usuario:str):
    """
    Valida que id_usuarios sea convertible a int
    Retorna True:False
    """
    patron=r"[0-9]+"
    return bool(re.fullmatch(patron, id_usuario))

def validar_nombre(nombre:str):
    """
    Valida que nombre sea u str valido
    Retorna True:False
    """
    # Definir un patron y un str y evaluar con de fullmatch
    patron = r"[a-zA-Z ]+" # completar
    return bool(re.fullmatch(patron, nombre))

def validar_email(email:str):
    """
    Valida que email sea un correo válido
    Retorna True:False"""
    # Definir un patron y un str y evaluar con de fullmatch
    patron = r"[a-zA-Z]+@\w+[\.\w]+" # completar
    return bool(re.fullmatch(patron, email))