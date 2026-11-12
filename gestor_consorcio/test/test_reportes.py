"""
Pruebas de src/reportes.py.

Las funciones de reportes son puras: reciben los datos como parámetro,
así que alcanza con armar un edificio chico en memoria (sin archivos).

Edificio de prueba:
    1A (60 %) de Ana Gómez y 1B (40 %) de Bruno Díaz.
    Enero 2026 ($1.000): ambas unidades pagaron.
    Febrero 2026 ($2.000): 1A pagó en dos cuotas, 1B no pagó (vence 10/03/2026).
"""
from datetime import date

from src import reportes


def datos_de_prueba():
    return {
        "propietarios": [
            {"dni": 30111222, "nombre": "Ana Gómez", "telefono": "1144556677", "email": "ana@mail.com"},
            {"dni": 27333444, "nombre": "Bruno Díaz", "telefono": "1155667788", "email": "bruno@mail.com"},
        ],
        "unidades": [
            {"codigo": "1B", "piso": 1, "porcentaje": 40.0, "dni": 27333444, "id_consorcio": 1},
            {"codigo": "1A", "piso": 1, "porcentaje": 60.0, "dni": 30111222, "id_consorcio": 1},
        ],
        "liquidaciones": [
            {"id_liquidacion": 1, "mes": 1, "anio": 2026, "total": 1000.0, "id_consorcio": 1},
            {"id_liquidacion": 2, "mes": 2, "anio": 2026, "total": 2000.0, "id_consorcio": 1},
        ],
        "gastos": [
            {"id_gasto": 1, "concepto": "limpieza", "monto": 700.0, "fecha": "2026-01-05", "id_liquidacion": 1},
            {"id_gasto": 2, "concepto": "luz", "monto": 300.0, "fecha": "2026-01-20", "id_liquidacion": 1},
            {"id_gasto": 3, "concepto": "limpieza", "monto": 800.0, "fecha": "2026-02-05", "id_liquidacion": 2},
            {"id_gasto": 4, "concepto": "ascensor", "monto": 1200.0, "fecha": "2026-02-15", "id_liquidacion": 2},
        ],
        "expensas": [
            {"id_expensa": 1, "importe": 600.0, "vencimiento": "2026-02-10", "codigo": "1A", "id_liquidacion": 1},
            {"id_expensa": 2, "importe": 400.0, "vencimiento": "2026-02-10", "codigo": "1B", "id_liquidacion": 1},
            {"id_expensa": 3, "importe": 1200.0, "vencimiento": "2026-03-10", "codigo": "1A", "id_liquidacion": 2},
            {"id_expensa": 4, "importe": 800.0, "vencimiento": "2026-03-10", "codigo": "1B", "id_liquidacion": 2},
        ],
        "pagos": [
            {"id_pago": 1, "fecha": "2026-02-05", "monto": 600.0, "medio_pago": "transferencia", "id_expensa": 1},
            {"id_pago": 2, "fecha": "2026-02-08", "monto": 400.0, "medio_pago": "efectivo", "id_expensa": 2},
            {"id_pago": 3, "fecha": "2026-03-01", "monto": 700.0, "medio_pago": "transferencia", "id_expensa": 3},
            {"id_pago": 4, "fecha": "2026-03-05", "monto": 500.0, "medio_pago": "débito", "id_expensa": 3},
        ],
    }


CORTE = date(2026, 5, 15)   # fecha de corte fija para que los tests no dependan del día de hoy


# ============================================================
# LIQUIDACIÓN
# ============================================================

def test_calcular_importes_reparte_segun_porcentaje():
    unidades = datos_de_prueba()["unidades"]
    assert reportes.calcular_importes(1000, unidades) == [("1B", 400.0), ("1A", 600.0)]


def test_suma_porcentajes():
    unidades = datos_de_prueba()["unidades"]
    assert reportes.suma_porcentajes(unidades) == 100
    assert reportes.suma_porcentajes(unidades, excepto="1A") == 40


def test_ordenar_unidades_por_piso_y_codigo():
    unidades = [{"codigo": "10A", "piso": 10}, {"codigo": "2B", "piso": 2}, {"codigo": "2A", "piso": 2}]
    assert [u["codigo"] for u in reportes.ordenar_unidades(unidades)] == ["2A", "2B", "10A"]


def test_buscar_liquidacion_y_esta_liquidada():
    datos = datos_de_prueba()
    liquidacion = reportes.buscar_liquidacion(datos["liquidaciones"], 2, 2026)
    assert liquidacion["id_liquidacion"] == 2
    assert reportes.buscar_liquidacion(datos["liquidaciones"], 3, 2026) is None
    assert reportes.esta_liquidada(2, datos["expensas"]) is True
    assert reportes.esta_liquidada(99, datos["expensas"]) is False


# ============================================================
# EXPENSAS Y PAGOS
# ============================================================

def test_total_pagado_suma_varios_pagos():
    pagos = datos_de_prueba()["pagos"]
    assert reportes.total_pagado(3, pagos) == 1200.0


def test_saldo_con_pago_parcial():
    datos = datos_de_prueba()
    solo_primer_pago = [p for p in datos["pagos"] if p["id_pago"] != 4]
    assert reportes.saldo_expensa(datos["expensas"][2], solo_primer_pago) == 500.0


def test_estado_expensa():
    datos = datos_de_prueba()
    expensa_paga, expensa_impaga = datos["expensas"][0], datos["expensas"][3]
    assert reportes.estado_expensa(expensa_paga, datos["pagos"], CORTE) == "Pagó"
    assert reportes.estado_expensa(expensa_impaga, datos["pagos"], CORTE) == "Debe"
    assert reportes.estado_expensa(expensa_impaga, datos["pagos"], date(2026, 3, 1)) == "Pendiente"


def test_detallar_expensas_hace_el_join():
    datos = datos_de_prueba()
    detalle = reportes.detallar_expensas(datos["expensas"], datos, CORTE)
    ultima = detalle[-1]                     # Feb 2026, unidad 1B
    assert ultima["codigo"] == "1B"
    assert ultima["propietario"] == "Bruno Díaz"
    assert (ultima["mes"], ultima["anio"]) == (2, 2026)
    assert ultima["saldo"] == 800.0
    assert ultima["estado"] == "Debe"


# ============================================================
# TABLA ANUAL
# ============================================================

def test_construir_tabla_anual():
    codigos, matriz = reportes.construir_tabla_anual(2026, datos_de_prueba(), CORTE)
    assert codigos == ["1A", "1B"]
    assert len(matriz) == 2 and len(matriz[0]) == 12
    assert matriz[0][:3] == ["Pagó", "Pagó", "-"]
    assert matriz[1][:3] == ["Pagó", "Debe", "-"]


def test_tabla_anual_de_otro_anio_queda_vacia():
    _, matriz = reportes.construir_tabla_anual(2025, datos_de_prueba(), CORTE)
    assert matriz == [["-"] * 12, ["-"] * 12]


def test_pagos_por_mes_usa_la_transpuesta():
    _, matriz = reportes.construir_tabla_anual(2026, datos_de_prueba(), CORTE)
    assert reportes.pagos_por_mes(matriz) == [2, 1] + [0] * 10


# ============================================================
# MOROSOS Y COBRANZA
# ============================================================

def test_deuda_con_recargo_por_mora():
    # 1B debe $800 de febrero (vencía 10/03). Al 15/05 lleva 2 meses: 800 x 3 % x 2 = 48
    deuda = reportes.calcular_deuda_unidad("1B", datos_de_prueba(), CORTE)
    assert deuda["meses"] == [(2, 2026)]
    assert deuda["saldo"] == 800.0
    assert deuda["recargo"] == 48.0
    assert deuda["total"] == 848.0
    assert deuda["atraso"] == 2


def test_recargo_minimo_un_mes():
    # Al día siguiente del vencimiento ya corre 1 mes de recargo: 800 x 3 % = 24
    deuda = reportes.calcular_deuda_unidad("1B", datos_de_prueba(), date(2026, 3, 11))
    assert deuda["recargo"] == 24.0


def test_unidad_al_dia_no_tiene_deuda():
    deuda = reportes.calcular_deuda_unidad("1A", datos_de_prueba(), CORTE)
    assert deuda["meses"] == []
    assert deuda["total"] == 0


def test_listar_morosos_ordena_de_mayor_a_menor():
    datos = datos_de_prueba()
    datos["pagos"] = [p for p in datos["pagos"] if p["id_pago"] != 4]   # 1A queda debiendo $500
    morosos = reportes.listar_morosos(datos, CORTE)
    assert [m["codigo"] for m in morosos] == ["1B", "1A"]
    assert morosos[0]["propietario"] == "Bruno Díaz"
    assert morosos[1]["total"] == 530.0   # 500 + 500 x 3 % x 2


def test_porcentaje_al_dia():
    datos = datos_de_prueba()
    morosos = reportes.listar_morosos(datos, CORTE)
    assert reportes.porcentaje_al_dia(datos, morosos) == (50.0, ["1A"], ["1B"])


def test_recaudacion_del_mes():
    datos = datos_de_prueba()
    resumen = reportes.recaudacion(datos["liquidaciones"][1], datos)
    assert resumen["liquidado"] == 2000.0
    assert resumen["cobrado"] == 1200.0
    assert resumen["pendiente"] == 800.0
    assert resumen["porcentaje"] == 60.0
    assert resumen["por_medio"]["transferencia"] == 700.0
    assert resumen["por_medio"]["débito"] == 500.0


# ============================================================
# GASTOS
# ============================================================

def test_gastos_por_categoria():
    totales, total = reportes.gastos_por_categoria(datos_de_prueba()["gastos"])
    assert totales == {"limpieza": 1500.0, "luz": 300.0, "ascensor": 1200.0, "mantenimiento": 0}
    assert total == 3000.0
