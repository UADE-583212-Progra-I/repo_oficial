from pathlib import Path

import src.interface as interface
import src.storage as storage

# Ruta al JSON construida a partir de la ubicación de ESTE archivo
# (src/services.py → sube a la raíz del proyecto → data/usuarios.json).
# Así funciona sin importar desde qué carpeta se ejecute el programa.
BASE_DIR = Path(__file__).resolve().parent
RUTA_USUARIOS = BASE_DIR.parent / "data" / "usuarios.json"


def listar_usuarios():
    """
    READ (todos): levanta el archivo JSON y retorna la lista de usuarios.
    """
    return storage.read_data(RUTA_USUARIOS)


def crear_usuario():
    """
    CREATE: da de alta un usuario.
    Colecta los campos desde la terminal (ya validados por interface),
    arma el diccionario, lo agrega a la lista cargada del JSON y persiste.
    Retorna True si se guardó, False si no.
    """
    usuarios = storage.read_data(RUTA_USUARIOS)

    id_usuario = interface.get_id_usuario()
    nombre = interface.get_nombre()
    email = interface.get_email()
    usuario = {
        "id_usuario": id_usuario,
        "nombre": nombre,
        "email": email,
    }
    usuarios.append(usuario)
    return storage.write_data(RUTA_USUARIOS, usuarios)


def buscar_usuario_por_id():
    """
    READ (uno): solicita el id del usuario a buscar.
    Retorna el diccionario del usuario o None.
    """
    usuarios = storage.read_data(RUTA_USUARIOS)
    id_usuario = interface.get_id_usuario()
    return next((u for u in usuarios if u["id_usuario"] == id_usuario), None)
