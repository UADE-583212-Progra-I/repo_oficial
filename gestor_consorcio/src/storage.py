"""
storage.py — Único punto de contacto entre el programa y el disco.

- JSON: una lista de diccionarios por entidad (data/propietarios.json, ...).
- TXT:  bitácora de operaciones en modo append (data/log.txt).
- CSV:  exportación de la tabla anual de pagos (lista de listas).

services.py NUNCA abre archivos directamente: llama a estas funciones.
Este módulo tampoco imprime: informa los problemas con el valor de
retorno o lanzando una excepción para que la capa de arriba decida qué mostrar.
"""
import csv
import json
import os
from datetime import datetime


def read_data(ruta):
    """
    Lee un archivo JSON y retorna su contenido como lista de diccionarios.

    Parámetros:
        ruta (str | Path): ruta al archivo JSON. Ej: data/usuarios.json
    Retorna:
        list: los registros del archivo, o [] si el archivo todavía no existe.
    Lanza:
        ValueError: si el archivo existe pero su contenido no es un JSON válido.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []   # como "CREATE TABLE IF NOT EXISTS": la tabla arranca vacía
    except json.JSONDecodeError as e:
        raise ValueError(f"El archivo {ruta} no tiene un JSON válido: {e}")


def write_data(ruta, datos):
    """
    Escribe una lista de diccionarios en un archivo JSON.
    Sobrescribe el contenido previo (reemplaza todo el archivo).

    Parámetros:
        ruta  (str | Path): ruta al archivo JSON.
        datos (list):       lista de diccionarios a persistir.
    Retorna:
        bool: True si se guardó correctamente, False si hubo un error.
    """
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False


def registrar_log(ruta, mensaje):
    """
    Agrega una línea con fecha y hora al final del archivo de log (modo "a").
    Si no se puede escribir, se ignora: el log nunca debe frenar el programa.
    """
    marca = datetime.now().isoformat(sep=" ", timespec="seconds")
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as file:
            file.write(f"[{marca}] {mensaje}\n")
    except OSError:
        pass


def exportar_csv(ruta, encabezados, filas):
    """
    Escribe una tabla (lista de listas) en un archivo CSV con encabezados.

    Retorna:
        bool: True si se exportó correctamente, False si hubo un error.
    """
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(encabezados)   # una fila
            writer.writerows(filas)        # todas las filas de una vez
        return True
    except OSError:
        return False
