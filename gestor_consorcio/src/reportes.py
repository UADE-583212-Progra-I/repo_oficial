"""
reportes.py — Cálculos del consorcio (funciones puras).

Reciben listas de diccionarios, o el diccionario `datos` con todas las
entidades ({"unidades": [...], "expensas": [...], ...}), y devuelven
resultados. No leen archivos ni imprimen, por eso se prueban fácilmente
con pytest (test/test_reportes.py).
"""
from datetime import date
from functools import reduce

from src import utils
from src.constantes import (CENTAVO, CONCEPTOS, ESTADO_DEUDA, ESTADO_PAGO,
                            ESTADO_PENDIENTE, MEDIOS_PAGO, RECARGO_MENSUAL,
                            SIN_EXPENSA)


# ============================================================
# BÚSQUEDAS Y AUXILIARES
# ============================================================

def buscar_liquidacion(liquidaciones, mes, anio):
    """Retorna la liquidación de ese mes y año, o None si no existe."""
    return next((l for l in liquidaciones if l["mes"] == mes and l["anio"] == anio), None)


def esta_liquidada(id_liquidacion, expensas):
    """Una liquidación está cerrada cuando ya generó sus expensas."""
    return next((e for e in expensas if e["id_liquidacion"] == id_liquidacion), None) is not None


def periodos(liquidaciones):
    """Diccionario id_liquidacion → (mes, anio), para hacer JOINs rápidos."""
    return {l["id_liquidacion"]: (l["mes"], l["anio"]) for l in liquidaciones}


def nombres_propietarios(propietarios):
    """Diccionario dni → nombre del propietario."""
    return {p["dni"]: p["nombre"] for p in propietarios}


def ordenar_unidades(unidades):
    """Ordena las unidades por piso y luego por código (1A, 1B, 2A, ..., 10A)."""
    return sorted(unidades, key=lambda u: (u["piso"], u["codigo"]))


def suma_porcentajes(unidades, excepto=""):
    """Suma los porcentajes de las unidades (opcionalmente sin contar una)."""
    porcentajes = [u["porcentaje"] for u in unidades if u["codigo"] != excepto]
    return round(reduce(lambda acc, p: acc + p, porcentajes, 0), 2)


# ============================================================
# LIQUIDACIÓN
# ============================================================

def calcular_importes(total, unidades):
    """
    Reparte el total de gastos entre las unidades según su porcentaje.
    Retorna una lista de tuplas (codigo, importe).
    """
    return [(u["codigo"], round(total * u["porcentaje"] / 100, 2)) for u in unidades]


# ============================================================
# EXPENSAS Y PAGOS
# ============================================================

def total_pagado(id_expensa, pagos):
    """Suma de todos los pagos de una expensa (puede tener más de uno)."""
    pagos_expensa = filter(lambda p: p["id_expensa"] == id_expensa, pagos)
    montos = list(map(lambda p: p["monto"], pagos_expensa))
    return round(reduce(lambda acc, m: acc + m, montos, 0), 2)


def saldo_expensa(expensa, pagos):
    """Lo que falta pagar de una expensa."""
    return round(expensa["importe"] - total_pagado(expensa["id_expensa"], pagos), 2)


def esta_vencida(expensa, fecha_corte):
    """True si la fecha de corte es posterior al vencimiento."""
    return date.fromisoformat(expensa["vencimiento"]) < fecha_corte


def estado_expensa(expensa, pagos, fecha_corte):
    """'Pagó' si no tiene saldo, 'Debe' si venció con saldo, 'Pendiente' si aún no venció."""
    if saldo_expensa(expensa, pagos) < CENTAVO:
        return ESTADO_PAGO
    if esta_vencida(expensa, fecha_corte):
        return ESTADO_DEUDA
    return ESTADO_PENDIENTE


def detallar_expensas(expensas, datos, fecha_corte):
    """
    JOIN manual: agrega a cada expensa el período, el propietario, el porcentaje,
    lo pagado, el saldo y el estado. Retorna una lista nueva (no modifica la original).
    """
    unidades = {u["codigo"]: u for u in datos["unidades"]}
    nombres = nombres_propietarios(datos["propietarios"])
    periodo = periodos(datos["liquidaciones"])
    pagos = datos["pagos"]

    detalle = []
    for e in expensas:
        unidad = unidades.get(e["codigo"], {})
        mes, anio = periodo[e["id_liquidacion"]]
        detalle.append({
            **e,
            "mes": mes,
            "anio": anio,
            "piso": unidad.get("piso", 0),
            "porcentaje": unidad.get("porcentaje", 0),
            "propietario": nombres.get(unidad.get("dni"), "Desconocido"),
            "pagado": total_pagado(e["id_expensa"], pagos),
            "saldo": saldo_expensa(e, pagos),
            "estado": estado_expensa(e, pagos, fecha_corte),
        })
    return sorted(detalle, key=lambda d: (d["anio"], d["mes"], d["piso"], d["codigo"]))


# ============================================================
# TABLA ANUAL DE PAGOS (matriz unidades x meses)
# ============================================================

def construir_tabla_anual(anio, datos, fecha_corte):
    """
    Construye la matriz de estados del año: cada fila es una unidad y cada
    columna un mes (12 columnas). Cada celda es 'Pagó', 'Debe', 'Pendiente'
    o '-' si ese mes no se liquidó.

    Retorna una tupla (codigos, matriz) donde codigos[i] es la unidad de la fila i.
    """
    mes_de = {l["id_liquidacion"]: l["mes"] for l in datos["liquidaciones"] if l["anio"] == anio}

    # Índice (codigo, mes) → expensa, para buscar cada celda en O(1)
    indice = {(e["codigo"], mes_de[e["id_liquidacion"]]): e
              for e in datos["expensas"] if e["id_liquidacion"] in mes_de}

    unidades = ordenar_unidades(datos["unidades"])
    matriz = [
        [estado_expensa(indice[(u["codigo"], mes)], datos["pagos"], fecha_corte)
         if (u["codigo"], mes) in indice else SIN_EXPENSA
         for mes in range(1, 13)]
        for u in unidades
    ]
    return [u["codigo"] for u in unidades], matriz


def pagos_por_mes(matriz):
    """
    Cuántas unidades pagaron cada mes. Trasponemos la matriz para que
    cada fila sea un mes y contamos los 'Pagó' con count().
    """
    return [columna.count(ESTADO_PAGO) for columna in utils.trasponer(matriz)]


# ============================================================
# MOROSOS Y COBRANZA
# ============================================================

def recargo_expensa(expensa, saldo, fecha_corte):
    """Recargo = saldo x RECARGO_MENSUAL x meses de atraso (mínimo 1 mes)."""
    atraso = max(1, utils.meses_entre(date.fromisoformat(expensa["vencimiento"]), fecha_corte))
    return saldo * RECARGO_MENSUAL * atraso


def calcular_deuda_unidad(codigo, datos, fecha_corte):
    """
    Revisa las expensas vencidas e impagas de una unidad.

    Retorna un diccionario con:
        meses   → lista de tuplas (mes, anio) adeudados, del más viejo al más nuevo
        saldo   → suma de lo adeudado
        recargo → recargo por mora
        total   → saldo + recargo
        atraso  → meses de atraso de la deuda más vieja (0 si no debe)
    """
    pagos = datos["pagos"]
    periodo = periodos(datos["liquidaciones"])

    vencidas = [e for e in datos["expensas"]
                if e["codigo"] == codigo
                and esta_vencida(e, fecha_corte)
                and saldo_expensa(e, pagos) >= CENTAVO]
    vencidas = sorted(vencidas, key=lambda e: e["vencimiento"])  # ISO: ordena por fecha

    saldo = reduce(lambda acc, e: acc + saldo_expensa(e, pagos), vencidas, 0)
    recargo = reduce(lambda acc, e: acc + recargo_expensa(e, saldo_expensa(e, pagos), fecha_corte),
                     vencidas, 0)
    atraso = 0
    if vencidas:
        atraso = max(1, utils.meses_entre(date.fromisoformat(vencidas[0]["vencimiento"]), fecha_corte))

    return {
        "codigo": codigo,
        "meses": [periodo[e["id_liquidacion"]] for e in vencidas],
        "saldo": round(saldo, 2),
        "recargo": round(recargo, 2),
        "total": round(saldo + recargo, 2),
        "atraso": atraso,
    }


def listar_morosos(datos, fecha_corte):
    """Unidades con deuda vencida, ordenadas de mayor a menor deuda total."""
    nombres = nombres_propietarios(datos["propietarios"])
    deudas = [{**calcular_deuda_unidad(u["codigo"], datos, fecha_corte),
               "propietario": nombres.get(u["dni"], "Desconocido")}
              for u in datos["unidades"]]
    con_deuda = filter(lambda d: len(d["meses"]) > 0, deudas)
    return sorted(con_deuda, key=lambda d: d["total"], reverse=True)


def porcentaje_al_dia(datos, morosos):
    """
    Qué porcentaje del edificio está al día, usando operaciones de conjuntos.
    Retorna una tupla (porcentaje, codigos_al_dia, codigos_con_deuda).
    """
    todas = {u["codigo"] for u in datos["unidades"]}
    con_deuda = {m["codigo"] for m in morosos} & todas   # intersección
    al_dia = todas - con_deuda                           # diferencia

    porcentaje = round(len(al_dia) / len(todas) * 100, 1) if todas else 0
    orden = lambda c: (utils.piso_de_codigo(c), c)
    return porcentaje, sorted(al_dia, key=orden), sorted(con_deuda, key=orden)


def recaudacion(liquidacion, datos):
    """Lo cobrado frente a lo liquidado en un mes, con el detalle por medio de pago."""
    expensas = [e for e in datos["expensas"] if e["id_liquidacion"] == liquidacion["id_liquidacion"]]
    ids = {e["id_expensa"] for e in expensas}
    pagos = [p for p in datos["pagos"] if p["id_expensa"] in ids]

    liquidado = round(reduce(lambda acc, e: acc + e["importe"], expensas, 0), 2)
    cobrado = round(reduce(lambda acc, p: acc + p["monto"], pagos, 0), 2)
    por_medio = {medio: round(sum([p["monto"] for p in pagos if p["medio_pago"] == medio]), 2)
                 for medio in MEDIOS_PAGO}

    return {
        "liquidado": liquidado,
        "cobrado": cobrado,
        "pendiente": round(liquidado - cobrado, 2),
        "porcentaje": round(cobrado / liquidado * 100, 1) if liquidado else 0,
        "por_medio": por_medio,
    }


# ============================================================
# GASTOS
# ============================================================

def gastos_por_categoria(gastos):
    """
    Suma los gastos por concepto.
    Retorna una tupla (totales, total) donde totales es {concepto: monto}.
    """
    totales = {c: round(sum([g["monto"] for g in gastos if g["concepto"] == c]), 2)
               for c in CONCEPTOS}
    total = round(sum(totales.values()), 2)
    return totales, total
