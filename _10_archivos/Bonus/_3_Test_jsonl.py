from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent
RUTA_DATA = BASE_DIR / "data"
ruta = os.path.join(RUTA_DATA, "usuarios.jsonl")

try:
    with open(ruta, "r", encoding="utf-8") as file:
        for linea in file:
            usuario = json.loads(linea)
            print(usuario)
except Exception as e:
    print(f"Error al leer {ruta}: {e}")