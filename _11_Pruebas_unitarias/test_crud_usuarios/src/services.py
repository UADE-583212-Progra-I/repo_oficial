from pathlib import Path
import src.interface as interface
import src.storage as storage

# Ruta al JSON construida a partir de la ubicación de ESTE archivo
# (src/services.py → sube a la raíz del proyecto → data/usuarios.json).
# Así funciona sin importar desde qué carpeta se ejecute el programa.
BASE_DIR = Path(__file__).resolve().parent
RUTA_USUARIOS = BASE_DIR.parent / "data" / "usuarios.json"

def generar_id_usuario(usuarios):
    """Genera y retorna el próximo id_usuario válido"""
    if not usuarios:
        return 1

    id_max = max(u["id_usuario"] for u in usuarios)
    return id_max + 1


def crear_usuario(nuevo_usuario):
    """Recibe el diccionario del nuevo_usuario, 
    lo agrega a la lista cargada del JSON y persiste.
    Retorna True si se guardó, False si no"""
    usuarios = storage.read_data(RUTA_USUARIOS)
    usuarios.append(nuevo_usuario)
    return storage.write_data(RUTA_USUARIOS, usuarios)


def listar_usuarios():
    """Levanta el archivo JSON y retorna la lista de usuarios"""
    return storage.read_data(RUTA_USUARIOS)


def buscar_usuario_por_id(id_usuario):
    """Recibe el id del usuario a buscar.
    Retorna el diccionario del usuario o None"""
    usuarios = storage.read_data(RUTA_USUARIOS)
    return next((u for u in usuarios if u["id_usuario"] == id_usuario), None)