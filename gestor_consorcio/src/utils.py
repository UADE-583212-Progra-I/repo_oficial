"""
utils.py — Funciones puras reutilizables.

- Validaciones de formato con expresiones regulares (re.fullmatch).
- Conversiones de fechas, montos y textos.
- Generación de ids, paginación y operaciones con matrices.

Ninguna función de este módulo lee archivos, pide datos ni imprime:
siempre devuelven el mismo resultado para los mismos argumentos.
"""
import re
from datetime import date

from src.constantes import DIA_VENCIMIENTO, MESES

# ============================================================
# PATRONES REGEX (siempre con r"" para que Python no procese las \)
# ============================================================

PATRON_ENTERO = r"[1-9][0-9]*"                       # 1, 42, 100 (no acepta 0)
PATRON_DNI = r"[1-9][0-9]{6,7}"                      # 7 u 8 dígitos, sin puntos
PATRON_NOMBRE = r"[A-Za-zÁÉÍÓÚáéíóúÜüÑñ ]+"          # letras, acentos, ñ y espacios
PATRON_EMAIL = r"[\w.+-]+@[\w-]+(\.[A-Za-z0-9-]+)+"  # acepta gmail.com y uade.edu.ar
PATRON_TELEFONO = r"\+?[0-9]{8,13}"                  # 1144556677 o +541144556677
PATRON_CUIT = r"(20|23|24|27|30|33|34)-[0-9]{8}-[0-9]"
PATRON_CODIGO = r"(PB|[1-9][0-9]?)[A-Z]"             # 1A, 10B, PBA (planta baja)
PATRON_DECIMAL = r"[0-9]+([.,][0-9]{1,2})?"          # 1500, 1500.5, 1500,50
PATRON_MES = r"(0?[1-9]|1[0-2])"                     # 1 a 12 (acepta 01)
PATRON_ANIO = r"20[0-9]{2}"                          # 2000 a 2099
PATRON_FECHA = r"[0-9]{2}/[0-9]{2}/[0-9]{4}"         # dd/mm/aaaa


# ============================================================
# VALIDACIONES — reciben un str y retornan True / False
# ============================================================

def validar_entero_positivo(valor: str) -> bool:
    """True si el texto es un entero mayor a 0 (sin signo ni decimales)."""
    return bool(re.fullmatch(PATRON_ENTERO, valor.strip()))


def validar_dni(dni: str) -> bool:
    """True si el DNI tiene 7 u 8 dígitos, sin puntos y sin empezar con 0."""
    return bool(re.fullmatch(PATRON_DNI, dni.strip()))


def validar_nombre(nombre: str) -> bool:
    """True si el nombre solo tiene letras (con acentos y ñ) y espacios."""
    return bool(re.fullmatch(PATRON_NOMBRE, nombre.strip()))


def validar_email(email: str) -> bool:
    """True si el email tiene usuario, @, dominio y al menos una extensión."""
    return bool(re.fullmatch(PATRON_EMAIL, email.strip()))


def validar_telefono(telefono: str) -> bool:
    """True si el teléfono tiene entre 8 y 13 dígitos (se ignoran espacios y guiones)."""
    limpio = telefono.strip().replace(" ", "").replace("-", "")
    return bool(re.fullmatch(PATRON_TELEFONO, limpio))


def validar_cuit(cuit: str) -> bool:
    """True si el CUIT tiene el formato XX-XXXXXXXX-X con un prefijo válido."""
    return bool(re.fullmatch(PATRON_CUIT, cuit.strip()))


def validar_codigo_unidad(codigo: str) -> bool:
    """True si el código es piso + letra (1A, 10B) o PB + letra (PBA)."""
    return bool(re.fullmatch(PATRON_CODIGO, codigo.strip().upper()))


def validar_monto(monto: str) -> bool:
    """True si el texto es un importe mayor a 0 con hasta 2 decimales."""
    if not re.fullmatch(PATRON_DECIMAL, monto.strip()):
        return False
    return convertir_decimal(monto) > 0


def validar_porcentaje(porcentaje: str) -> bool:
    """True si el texto es un número mayor a 0 y menor o igual a 100."""
    if not re.fullmatch(PATRON_DECIMAL, porcentaje.strip()):
        return False
    return 0 < convertir_decimal(porcentaje) <= 100


def validar_mes(mes: str) -> bool:
    """True si el texto es un mes del 1 al 12."""
    return bool(re.fullmatch(PATRON_MES, mes.strip()))


def validar_anio(anio: str) -> bool:
    """True si el texto es un año entre 2000 y 2099."""
    return bool(re.fullmatch(PATRON_ANIO, anio.strip()))


def validar_fecha(texto: str) -> bool:
    """True si el texto es una fecha real con formato dd/mm/aaaa."""
    try:
        texto_a_fecha(texto)
        return True
    except ValueError:
        return False


# ============================================================
# CONVERSIONES
# ============================================================

def convertir_decimal(texto: str) -> float:
    """Convierte '1500,50' o '1500.50' a 1500.5 (sin separador de miles)."""
    return float(texto.strip().replace(",", "."))


def normalizar_nombre(nombre: str) -> str:
    """Quita espacios de más y pone mayúscula en cada palabra: ' ana  gómez' → 'Ana Gómez'."""
    return " ".join(nombre.split()).title()


def texto_a_fecha(texto: str) -> date:
    """
    Convierte 'dd/mm/aaaa' en un objeto date.
    Lanza ValueError si el formato es incorrecto o la fecha no existe (ej: 31/02/2026).
    """
    texto = texto.strip()
    if not re.fullmatch(PATRON_FECHA, texto):
        raise ValueError("La fecha debe tener el formato dd/mm/aaaa.")
    dia, mes, anio = texto.split("/")          # unpacking de la lista
    return date(int(anio), int(mes), int(dia))  # date() lanza ValueError si no existe


def fecha_a_texto(fecha) -> str:
    """Convierte un date (o un texto ISO 'aaaa-mm-dd' del JSON) a 'dd/mm/aaaa'."""
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha)
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year}"


def formatear_moneda(monto: float) -> str:
    """Formato argentino: 1234567.5 → '$1.234.567,50'."""
    texto = f"{monto:,.2f}"                    # '1,234,567.50' (formato inglés)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${texto}"


def formatear_porcentaje(valor: float, decimales: int = 1) -> str:
    """Formato argentino: 12.5 → '12,5%'."""
    return f"{valor:.{decimales}f}%".replace(".", ",")


def nombre_mes(mes: int) -> str:
    """1 → 'Ene', 12 → 'Dic'."""
    return MESES[mes - 1]


def periodo_texto(mes: int, anio: int) -> str:
    """(7, 2026) → 'Jul 2026'."""
    return f"{nombre_mes(mes)} {anio}"


def piso_de_codigo(codigo: str) -> int:
    """Obtiene el piso a partir del código con slicing: '10B' → 10, 'PBA' → 0."""
    codigo = codigo.strip().upper()
    if codigo.startswith("PB"):
        return 0
    return int(codigo[:-1])   # todo menos la última letra


# ============================================================
# FECHAS DE NEGOCIO
# ============================================================

def calcular_vencimiento(mes: int, anio: int) -> date:
    """La expensa de un mes vence el DIA_VENCIMIENTO del mes siguiente."""
    if mes == 12:
        return date(anio + 1, 1, DIA_VENCIMIENTO)
    return date(anio, mes + 1, DIA_VENCIMIENTO)


def meses_entre(desde: date, hasta: date) -> int:
    """Cantidad de meses calendario entre dos fechas: (10/07, 12/11) → 4."""
    return (hasta.year - desde.year) * 12 + (hasta.month - desde.month)


# ============================================================
# LISTAS Y MATRICES
# ============================================================

def generar_id(lista: list, campo: str) -> int:
    """Retorna el próximo id libre de una lista de diccionarios (max + 1, o 1 si está vacía)."""
    if not lista:
        return 1
    return max([registro[campo] for registro in lista]) + 1


def paginar(lista: list, pagina: int, tamanio: int) -> list:
    """Devuelve los registros de una página usando slicing (la página 1 es la primera)."""
    inicio = (pagina - 1) * tamanio
    return lista[inicio:inicio + tamanio]


def total_paginas(cantidad: int, tamanio: int) -> int:
    """Cantidad de páginas necesarias para mostrar 'cantidad' registros (mínimo 1)."""
    if cantidad == 0:
        return 1
    return (cantidad + tamanio - 1) // tamanio   # división entera redondeando hacia arriba


def trasponer(matriz: list) -> list:
    """
    Retorna la transpuesta de una matriz n x m (las filas pasan a ser columnas).
    Se usa para recorrer la tabla anual de pagos por mes en lugar de por unidad.
    """
    if not matriz:
        return []
    return [[fila[j] for fila in matriz] for j in range(len(matriz[0]))]
