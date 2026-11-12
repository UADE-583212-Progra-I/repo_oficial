"""
Pruebas de src/utils.py: validaciones con regex, conversiones y matrices.
Patrón AAA (Arrange - Act - Assert) y @pytest.mark.parametrize para
probar muchos casos (happy path y sad path) con un solo test.
"""
from datetime import date

import pytest

from src import utils


# ============================================================
# VALIDACIONES
# ============================================================

@pytest.mark.parametrize("valor, esperado", [
    ("1", True), ("42", True), ("100", True),
    ("0", False), ("-3", False), ("3.5", False), ("abc", False), ("", False),
])
def test_validar_entero_positivo(valor, esperado):
    assert utils.validar_entero_positivo(valor) == esperado


@pytest.mark.parametrize("dni, esperado", [
    ("30123456", True), ("1234567", True), (" 30123456 ", True),
    ("0123456", False), ("30.123.456", False), ("123456", False),
    ("123456789", False), ("abc", False), ("", False),
])
def test_validar_dni(dni, esperado):
    assert utils.validar_dni(dni) == esperado


@pytest.mark.parametrize("nombre, esperado", [
    ("Carlos", True), ("María", True), ("Ana García", True), ("José María Núñez", True),
    ("ana123", False), ("Pedro!", False), ("", False), ("   ", False),
])
def test_validar_nombre(nombre, esperado):
    assert utils.validar_nombre(nombre) == esperado


@pytest.mark.parametrize("email, esperado", [
    # Happy path
    ("username@mail.com", True),
    ("username.lastname@mail.com", True),
    ("username@mail.com.ar", True),
    ("username1@mail.com", True),
    # Sad path
    ("username.com", False),
    ("username@mail", False),
    ("@mail.com", False),
    ("doble@@mail.com", False),
    ("", False),
])
def test_validar_email(email, esperado):
    assert utils.validar_email(email) == esperado


@pytest.mark.parametrize("telefono, esperado", [
    ("1144556677", True), ("11-4455-6677", True), ("+541144556677", True),
    ("1234", False), ("telefono", False), ("", False),
])
def test_validar_telefono(telefono, esperado):
    assert utils.validar_telefono(telefono) == esperado


@pytest.mark.parametrize("cuit, esperado", [
    ("30-71234567-8", True), ("20-12345678-9", True),
    ("30712345678", False), ("99-12345678-9", False), ("30-1234567-8", False), ("", False),
])
def test_validar_cuit(cuit, esperado):
    assert utils.validar_cuit(cuit) == esperado


@pytest.mark.parametrize("codigo, esperado", [
    ("1A", True), ("10B", True), ("PBA", True), ("2b", True),
    ("A1", False), ("0A", False), ("1", False), ("1AB", False), ("", False),
])
def test_validar_codigo_unidad(codigo, esperado):
    assert utils.validar_codigo_unidad(codigo) == esperado


@pytest.mark.parametrize("monto, esperado", [
    ("1500", True), ("1500.5", True), ("1500,50", True),
    ("0", False), ("-10", False), ("1.500,50", False), ("10.123", False), ("abc", False), ("", False),
])
def test_validar_monto(monto, esperado):
    assert utils.validar_monto(monto) == esperado


@pytest.mark.parametrize("porcentaje, esperado", [
    ("15", True), ("17.5", True), ("100", True),
    ("0", False), ("100.01", False), ("150", False), ("abc", False),
])
def test_validar_porcentaje(porcentaje, esperado):
    assert utils.validar_porcentaje(porcentaje) == esperado


@pytest.mark.parametrize("mes, esperado", [
    ("1", True), ("01", True), ("12", True), ("0", False), ("13", False), ("", False),
])
def test_validar_mes(mes, esperado):
    assert utils.validar_mes(mes) == esperado


@pytest.mark.parametrize("fecha, esperado", [
    ("12/11/2026", True), ("29/02/2028", True),
    ("31/02/2026", False),     # el formato es correcto pero la fecha no existe
    ("2026-11-12", False), ("1/1/2026", False), ("", False),
])
def test_validar_fecha(fecha, esperado):
    assert utils.validar_fecha(fecha) == esperado


# ============================================================
# CONVERSIONES
# ============================================================

def test_texto_a_fecha():
    assert utils.texto_a_fecha("05/07/2026") == date(2026, 7, 5)


def test_texto_a_fecha_invalida_lanza_error():
    with pytest.raises(ValueError):
        utils.texto_a_fecha("31/02/2026")


def test_fecha_a_texto_desde_date_y_desde_iso():
    assert utils.fecha_a_texto(date(2026, 7, 5)) == "05/07/2026"
    assert utils.fecha_a_texto("2026-07-05") == "05/07/2026"


@pytest.mark.parametrize("monto, esperado", [
    (1234.5, "$1.234,50"), (0, "$0,00"), (1000000, "$1.000.000,00"), (99.999, "$100,00"),
])
def test_formatear_moneda(monto, esperado):
    assert utils.formatear_moneda(monto) == esperado


def test_formatear_porcentaje():
    assert utils.formatear_porcentaje(12.5) == "12,5%"
    assert utils.formatear_porcentaje(15, 2) == "15,00%"


def test_normalizar_nombre():
    assert utils.normalizar_nombre("  maría   gonzález ") == "María González"


@pytest.mark.parametrize("codigo, piso", [("1A", 1), ("10B", 10), ("PBA", 0), ("3c", 3)])
def test_piso_de_codigo(codigo, piso):
    assert utils.piso_de_codigo(codigo) == piso


def test_convertir_decimal_acepta_coma_y_punto():
    assert utils.convertir_decimal("1500,50") == 1500.5
    assert utils.convertir_decimal("1500.50") == 1500.5


# ============================================================
# FECHAS DE NEGOCIO
# ============================================================

@pytest.mark.parametrize("mes, anio, esperado", [
    (6, 2026, date(2026, 7, 10)),
    (12, 2026, date(2027, 1, 10)),   # diciembre vence en enero del año siguiente
])
def test_calcular_vencimiento(mes, anio, esperado):
    assert utils.calcular_vencimiento(mes, anio) == esperado


def test_meses_entre():
    assert utils.meses_entre(date(2026, 7, 10), date(2026, 11, 12)) == 4
    assert utils.meses_entre(date(2025, 12, 10), date(2026, 1, 5)) == 1
    assert utils.meses_entre(date(2026, 7, 10), date(2026, 7, 20)) == 0


# ============================================================
# LISTAS Y MATRICES
# ============================================================

def test_generar_id_lista_vacia():
    assert utils.generar_id([], "id_pago") == 1


def test_generar_id_usa_el_maximo():
    pagos = [{"id_pago": 3}, {"id_pago": 7}, {"id_pago": 5}]
    assert utils.generar_id(pagos, "id_pago") == 8


def test_paginar():
    numeros = list(range(1, 13))   # 12 elementos
    assert utils.paginar(numeros, 1, 5) == [1, 2, 3, 4, 5]
    assert utils.paginar(numeros, 3, 5) == [11, 12]
    assert utils.paginar(numeros, 4, 5) == []


@pytest.mark.parametrize("cantidad, paginas", [(0, 1), (5, 1), (6, 2), (12, 3)])
def test_total_paginas(cantidad, paginas):
    assert utils.total_paginas(cantidad, 5) == paginas


def test_trasponer():
    matriz = [[1, 2, 3],
              [4, 5, 6]]
    assert utils.trasponer(matriz) == [[1, 4], [2, 5], [3, 6]]


def test_trasponer_dos_veces_devuelve_la_original():
    matriz = [[1, 2], [3, 4], [5, 6]]
    assert utils.trasponer(utils.trasponer(matriz)) == matriz


def test_trasponer_matriz_vacia():
    assert utils.trasponer([]) == []
