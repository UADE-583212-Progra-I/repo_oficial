"""
Pruebas de src/services.py con mocking.

services.py lee y escribe archivos a través de storage. En un test no
queremos tocar el disco, así que reemplazamos (patch) las funciones de
storage por versiones falsas que trabajan con datos en memoria.

Regla: el patch apunta a donde la función SE USA ("src.services.storage..."),
no a donde se define.
"""
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from src import services
from test.test_reportes import datos_de_prueba

LEER = "src.services.storage.read_data"
ESCRIBIR = "src.services.storage.write_data"
LOG = "src.services.storage.registrar_log"


def leer_falso(datos):
    """
    Reemplazo de storage.read_data: según el nombre del archivo
    (data/unidades.json → 'unidades') devuelve una copia de esa lista.
    """
    return lambda ruta: [dict(registro) for registro in datos.get(Path(ruta).stem, [])]


def lo_guardado(mock_write, entidad):
    """Lista que services intentó guardar para una entidad (la última vez)."""
    llamadas = [c for c in mock_write.call_args_list if Path(c.args[0]).stem == entidad]
    return llamadas[-1].args[1]


# ============================================================
# PROPIETARIOS
# ============================================================

def test_crear_propietario_normaliza_y_guarda():
    # Arrange
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        # Act
        nuevo = services.crear_propietario(40123456, "  carla   ruiz ", "11-4455-6677", "Carla@Mail.com")

        # Assert
        assert nuevo["nombre"] == "Carla Ruiz"
        assert nuevo["telefono"] == "1144556677"
        assert nuevo["email"] == "carla@mail.com"
        guardados = lo_guardado(mock_write, "propietarios")
        assert len(guardados) == 3
        assert guardados[-1]["dni"] == 40123456


def test_crear_propietario_con_dni_repetido_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        with pytest.raises(ValueError, match="Ya existe"):
            services.crear_propietario(30111222, "Otra Persona", "1144556677", "otra@mail.com")
        mock_write.assert_not_called()


def test_crear_propietario_con_email_invalido_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="email"):
            services.crear_propietario(40123456, "Carla Ruiz", "1144556677", "carla@mail")


def test_eliminar_propietario_con_unidades_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        with pytest.raises(ValueError, match="1A"):
            services.eliminar_propietario(30111222)
        mock_write.assert_not_called()


def test_buscar_propietarios_por_nombre_con_regex():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)):
        assert [p["nombre"] for p in services.buscar_propietarios_por_nombre("^bru")] == ["Bruno Díaz"]
        assert services.buscar_propietarios_por_nombre("xyz") == []


def test_buscar_propietarios_con_patron_invalido_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)):
        with pytest.raises(ValueError, match="patrón"):
            services.buscar_propietarios_por_nombre("(")


# ============================================================
# UNIDADES
# ============================================================

def test_crear_unidad_que_supera_el_100_por_ciento_falla():
    datos = datos_de_prueba()   # 1A + 1B ya suman 100 %
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="sumaría"):
            services.crear_unidad("2A", 10, 30111222)


def test_crear_unidad_calcula_el_piso():
    datos = datos_de_prueba()
    datos["unidades"][0]["porcentaje"] = 30.0   # 1B baja de 40 % a 30 %: quedan 10 % libres
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        unidad = services.crear_unidad("12c", 10, 27333444)
        assert unidad["codigo"] == "12C"
        assert unidad["piso"] == 12
        assert lo_guardado(mock_write, "unidades")[-1] == unidad


def test_crear_unidad_con_propietario_inexistente_falla():
    datos = datos_de_prueba()
    datos["unidades"] = []
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="No existe un propietario"):
            services.crear_unidad("2A", 10, 11111111)


def test_eliminar_unidad_con_expensas_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="expensas"):
            services.eliminar_unidad("1A")


# ============================================================
# GASTOS Y LIQUIDACIONES
# ============================================================

def test_cargar_gasto_en_mes_nuevo_crea_la_liquidacion():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        gasto = services.cargar_gasto(3, 2026, "Luz", 450.0, date(2026, 3, 8))

        liquidaciones = lo_guardado(mock_write, "liquidaciones")
        assert liquidaciones[-1] == {"id_liquidacion": 3, "mes": 3, "anio": 2026,
                                     "total": 0, "id_consorcio": 1}
        assert gasto["id_liquidacion"] == 3
        assert gasto["concepto"] == "luz"
        assert gasto["fecha"] == "2026-03-08"


def test_cargar_gasto_en_mes_liquidado_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="ya fue liquidado"):
            services.cargar_gasto(2, 2026, "luz", 100.0, date(2026, 2, 20))


def test_cargar_gasto_con_concepto_invalido_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="Concepto"):
            services.cargar_gasto(3, 2026, "seguridad", 100.0, date(2026, 3, 1))


def test_liquidar_mes_emite_una_expensa_por_unidad():
    # Arrange: marzo abierto con $3.000 de gastos
    datos = datos_de_prueba()
    datos["liquidaciones"].append({"id_liquidacion": 3, "mes": 3, "anio": 2026, "total": 0, "id_consorcio": 1})
    datos["gastos"] += [
        {"id_gasto": 5, "concepto": "limpieza", "monto": 1000.0, "fecha": "2026-03-05", "id_liquidacion": 3},
        {"id_gasto": 6, "concepto": "mantenimiento", "monto": 2000.0, "fecha": "2026-03-20", "id_liquidacion": 3},
    ]
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        # Act
        liquidacion, emitidas = services.liquidar_mes(3, 2026)

        # Assert
        assert liquidacion["total"] == 3000.0
        assert [(e["codigo"], e["importe"]) for e in emitidas] == [("1A", 1800.0), ("1B", 1200.0)]
        assert all([e["vencimiento"] == "2026-04-10" for e in emitidas])
        assert [e["id_expensa"] for e in emitidas] == [5, 6]
        assert len(lo_guardado(mock_write, "expensas")) == 6


def test_liquidar_mes_ya_liquidado_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="ya fue liquidado"):
            services.liquidar_mes(2, 2026)


def test_liquidar_mes_con_porcentajes_incompletos_falla():
    datos = datos_de_prueba()
    datos["unidades"][0]["porcentaje"] = 30.0   # el edificio suma 90 %
    datos["liquidaciones"].append({"id_liquidacion": 3, "mes": 3, "anio": 2026, "total": 0, "id_consorcio": 1})
    datos["gastos"].append({"id_gasto": 5, "concepto": "luz", "monto": 100.0,
                            "fecha": "2026-03-05", "id_liquidacion": 3})
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="deben sumar 100"):
            services.liquidar_mes(3, 2026)


# ============================================================
# PAGOS
# ============================================================

def test_registrar_pago_parcial_devuelve_el_saldo():
    datos = datos_de_prueba()   # la expensa 4 (1B, febrero) debe $800
    with patch(LEER, side_effect=leer_falso(datos)), \
         patch(ESCRIBIR, return_value=True) as mock_write, patch(LOG):
        pago, saldo = services.registrar_pago(4, 300.0, "Efectivo", date(2026, 3, 20))
        assert saldo == 500.0
        assert pago["id_pago"] == 5
        assert pago["medio_pago"] == "efectivo"
        assert lo_guardado(mock_write, "pagos")[-1] == pago


def test_registrar_pago_mayor_al_saldo_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="supera el saldo"):
            services.registrar_pago(4, 900.0, "efectivo", date(2026, 3, 20))


def test_registrar_pago_de_expensa_ya_paga_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="ya está paga"):
            services.registrar_pago(1, 10.0, "efectivo", date(2026, 3, 20))


def test_registrar_pago_con_medio_invalido_falla():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=True), patch(LOG):
        with pytest.raises(ValueError, match="Medio de pago"):
            services.registrar_pago(4, 100.0, "cheque", date(2026, 3, 20))


# ============================================================
# ERRORES DE ARCHIVOS
# ============================================================

def test_si_no_se_puede_guardar_lanza_oserror():
    datos = datos_de_prueba()
    with patch(LEER, side_effect=leer_falso(datos)), patch(ESCRIBIR, return_value=False), patch(LOG):
        with pytest.raises(OSError):
            services.crear_propietario(40123456, "Carla Ruiz", "1144556677", "carla@mail.com")
