# # Cambia la ruta desde donde ejecutas el script
# Y verificar si encuentra o no la carpeta data

import os

# Ver el directorio de trabajo actual
print("Directorio actual (cwd):", os.getcwd())

# Verificar si un archivo o carpeta existe
print("¿Existe la carpeta 'data' (con cwd)?", os.path.exists("data"))

# Construir rutas con os.path.join
# Esto funciona en Windows, Mac y Linux sin cambios
if os.path.exists("data"):
    ruta = os.path.join("data", "usuarios.json")
    print("Ruta construida:", ruta)



from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
RUTA_DATA = BASE_DIR / "data"

# Verificar si un archivo o carpeta existe
print("¿Existe la carpeta 'data' (con path)?", os.path.exists(RUTA_DATA))



try:
    file = open("data/test.txt", "r", encoding="utf-8")
    # print(file)
    file.write("Hola desde file\n")
    file.close()
except Exception as e:
    print(f"ERROR capturado con try: {e}")


try:
    with open("data/test.txt", "w", encoding="utf-8") as file:
        file.write("Hola desde with\n")
except Exception as e:
    print(e)