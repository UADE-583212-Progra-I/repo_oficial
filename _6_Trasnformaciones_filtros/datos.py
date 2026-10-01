"""
Para nuestra actividad de lambda y listas por comprensión, necesitamos datos.
Por ello vamos a trabajar con este dataset
https://www.kaggle.com/datasets/sahilislam007/ai-impact-on-job-market-20242030?resource=download
"""

# Importamos librerias externas
import csv
import urllib.request
from tabulate import tabulate

# URL del dataset en el Repo del curso en GitHub
url = "https://raw.githubusercontent.com/UADE-Progra-I/565944_repo_oficial/refs/heads/main/Datasets/ai_job_trends.csv"


# Función que importa los datos
def load_data(url, limit=None):
    datos = []  # lista de diccionarios con datos importados
    # Leemos el csv con la libreria
    with urllib.request.urlopen(url) as response:
        lineas = [l.decode("utf-8") for l in response.readlines()]
        reader = csv.DictReader(lineas)

    # Generamos la lista de diccionarios como estructura de datos del csv
    for i, fila in enumerate(reader):
        if i == limit:
            break
        datos.append(fila)
    return datos


# Importar datos
datos_raw = load_data(url, 10)

# Exploremos la estructura de datos
print(f"datos type: {type(datos_raw)}")
print(f"datos length: {len(datos_raw)} registros")
print(f"datos registro type: {type(datos_raw[0])}")

# Exploremos las columnas del dataset
# col = datos_raw[0].keys()
# for i, v in enumerate(col):
#     print(f"Col {i}: {v}")

# Seleccionemos columnas relevantes
# 1: Job Title, 2: AI Impact Level, 3: Median Salary (USD)
datos = [
    {
        "job_title": d.get("Job Title"),
        "ai_impact": d.get("AI Impact Level"),
        "salary": d.get("Median Salary (USD)"),
    }
    for d in datos_raw
]


# print(tabulate(datos[:5], headers="keys", tablefmt="grid"))