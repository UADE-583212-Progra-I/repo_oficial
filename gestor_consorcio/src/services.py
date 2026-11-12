"""
services.py — Lógica de negocio del consorcio.

- Lee y guarda los datos a través de storage (nunca abre archivos directamente).
  Usa la estrategia "leer y escribir en cada operación": el JSON siempre
  refleja el estado real aunque el programa se corte.
- Valida las reglas del negocio y lanza ValueError cuando no se cumplen.
- No usa input() ni print(): eso es trabajo de interface.py.
"""
import re
from datetime import date
from functools import reduce
from pathlib import Path

from src import reportes, storage, utils
from src.constantes import CENTAVO, CONCEPTOS, ID_CONSORCIO, MEDIOS_PAGO, MESES

# Rutas construidas a partir de la ubicación de ESTE archivo
# (src/services.py → sube a la raíz del proyecto → data/).
# Así el programa encuentra los JSON sin importar desde dónde se ejecute.
BASE_DIR = Path(__file__).resolve().parent
RUTA_DATA = BASE_DIR.parent / "data"

ENTIDADES = ("consorcios", "propietarios", "unidades", "liquidaciones",
             "gastos", "expensas", "pagos")
RUTAS = {entidad: RUTA_DATA / f"{entidad}.json" for entidad in ENTIDADES}
RUTA_LOG = RUTA_DATA / "log.txt"


# ============================================================
# ACCESO A DATOS
# ============================================================

def leer(entidad):
    """Retorna la lista de registros de una entidad (ej: 'unidades')."""
    return storage.read_data(RUTAS[entidad])


def guardar(entidad, datos):
    """Persiste la lista de registros de una entidad. Lanza OSError si falla."""
    if not storage.write_data(RUTAS[entidad], datos):
        raise OSError(f"No se pudo guardar el archivo {RUTAS[entidad].name}.")


def registrar(mensaje):
    """Deja constancia de una operación en data/log.txt."""
    storage.registrar_log(RUTA_LOG, mensaje)


def cargar_datos():
    """Todas las entidades en un diccionario {entidad: lista}, para los reportes."""
    return {entidad: leer(entidad) for entidad in ENTIDADES}


def fecha_o_hoy(fecha_corte):
    """Los reportes usan la fecha de hoy salvo que se indique otra (útil en los tests)."""
    return fecha_corte if fecha_corte else date.today()


# ============================================================
# CONSORCIO
# ============================================================

def obtener_consorcio():
    """Retorna el diccionario del consorcio o None si todavía no se cargó."""
    return next((c for c in leer("consorcios") if c["id_consorcio"] == ID_CONSORCIO), None)


def modificar_consorcio(nombre="", direccion="", cuit=""):
    """Actualiza los datos del consorcio. Los campos vacíos no se modifican."""
    if cuit and not utils.validar_cuit(cuit):
        raise ValueError("CUIT inválido. Formato esperado: 30-12345678-9.")

    consorcios = leer("consorcios")
    consorcio = next((c for c in consorcios if c["id_consorcio"] == ID_CONSORCIO), None)
    if consorcio is None:
        consorcio = {"id_consorcio": ID_CONSORCIO, "nombre": "", "direccion": "", "cuit": ""}
        consorcios.append(consorcio)

    if nombre.strip():
        consorcio["nombre"] = nombre.strip()
    if direccion.strip():
        consorcio["direccion"] = direccion.strip()
    if cuit.strip():
        consorcio["cuit"] = cuit.strip()

    guardar("consorcios", consorcios)
    registrar("Datos del consorcio actualizados")
    return consorcio


# ============================================================
# CRUD DE PROPIETARIOS
# ============================================================

def listar_propietarios():
    """Todos los propietarios ordenados alfabéticamente."""
    return sorted(leer("propietarios"), key=lambda p: p["nombre"])


def buscar_propietario(dni):
    """Retorna el propietario con ese DNI o None."""
    return next((p for p in leer("propietarios") if p["dni"] == dni), None)


def buscar_propietarios_por_nombre(texto):
    """Búsqueda parcial con re.search, sin distinguir mayúsculas (acepta patrones como '^Mar')."""
    try:
        return [p for p in listar_propietarios() if re.search(texto, p["nombre"], re.IGNORECASE)]
    except re.error:
        raise ValueError(f"'{texto}' no es un patrón de búsqueda válido.")


def unidades_de_propietario(dni):
    """Códigos de las unidades de un propietario (puede tener varias)."""
    unidades = reportes.ordenar_unidades(leer("unidades"))
    return [u["codigo"] for u in unidades if u["dni"] == dni]


def validar_datos_propietario(nombre, telefono, email):
    """Valida el formato de los datos de contacto. Lanza ValueError si alguno es inválido."""
    if not utils.validar_nombre(nombre):
        raise ValueError("El nombre solo puede contener letras y espacios.")
    if not utils.validar_telefono(telefono):
        raise ValueError("El teléfono debe tener entre 8 y 13 dígitos.")
    if not utils.validar_email(email):
        raise ValueError("El email no es válido.")


def crear_propietario(dni, nombre, telefono, email):
    """CREATE: da de alta un propietario. El DNI no se puede repetir."""
    if not utils.validar_dni(str(dni)):
        raise ValueError("El DNI debe tener 7 u 8 dígitos.")
    validar_datos_propietario(nombre, telefono, email)

    propietarios = leer("propietarios")
    if next((p for p in propietarios if p["dni"] == dni), None) is not None:
        raise ValueError(f"Ya existe un propietario con DNI {dni}.")

    propietario = {
        "dni": dni,
        "nombre": utils.normalizar_nombre(nombre),
        "telefono": telefono.strip().replace(" ", "").replace("-", ""),
        "email": email.strip().lower(),
    }
    propietarios.append(propietario)
    guardar("propietarios", propietarios)
    registrar(f"Propietario creado: {propietario['nombre']} (DNI {dni})")
    return propietario


def modificar_propietario(dni, nombre="", telefono="", email=""):
    """UPDATE: modifica los datos de contacto. Los campos vacíos se mantienen."""
    propietarios = leer("propietarios")
    propietario = next((p for p in propietarios if p["dni"] == dni), None)
    if propietario is None:
        raise ValueError(f"No existe un propietario con DNI {dni}.")

    # Si un campo viene vacío, se valida con el valor que ya tenía
    nuevo_nombre = nombre if nombre.strip() else propietario["nombre"]
    nuevo_telefono = telefono if telefono.strip() else propietario["telefono"]
    nuevo_email = email if email.strip() else propietario["email"]
    validar_datos_propietario(nuevo_nombre, nuevo_telefono, nuevo_email)

    propietario["nombre"] = utils.normalizar_nombre(nuevo_nombre)
    propietario["telefono"] = nuevo_telefono.strip().replace(" ", "").replace("-", "")
    propietario["email"] = nuevo_email.strip().lower()

    guardar("propietarios", propietarios)
    registrar(f"Propietario modificado: DNI {dni}")
    return propietario


def eliminar_propietario(dni):
    """DELETE: no se puede eliminar a quien todavía es dueño de alguna unidad."""
    propietarios = leer("propietarios")
    propietario = next((p for p in propietarios if p["dni"] == dni), None)
    if propietario is None:
        raise ValueError(f"No existe un propietario con DNI {dni}.")

    codigos = unidades_de_propietario(dni)
    if codigos:
        raise ValueError(f"No se puede eliminar: es dueño de {', '.join(codigos)}. "
                         "Primero asigná esas unidades a otro propietario.")

    propietarios.remove(propietario)
    guardar("propietarios", propietarios)
    registrar(f"Propietario eliminado: {propietario['nombre']} (DNI {dni})")
    return propietario


# ============================================================
# CRUD DE UNIDADES
# ============================================================

def listar_unidades():
    """Unidades ordenadas por piso, con el nombre del propietario (JOIN manual)."""
    nombres = reportes.nombres_propietarios(leer("propietarios"))
    return [{**u, "propietario": nombres.get(u["dni"], "Desconocido")}
            for u in reportes.ordenar_unidades(leer("unidades"))]


def buscar_unidad(codigo):
    """Retorna la unidad con ese código o None."""
    codigo = codigo.strip().upper()
    return next((u for u in leer("unidades") if u["codigo"] == codigo), None)


def porcentaje_disponible(excepto=""):
    """Cuánto porcentaje del edificio queda sin asignar."""
    return round(100 - reportes.suma_porcentajes(leer("unidades"), excepto), 2)


def validar_porcentaje_unidad(unidades, codigo, porcentaje):
    """El porcentaje debe ser > 0 y el edificio no puede superar el 100 %."""
    if not 0 < porcentaje <= 100:
        raise ValueError("El porcentaje debe ser mayor a 0 y menor o igual a 100.")
    asignado = reportes.suma_porcentajes(unidades, excepto=codigo)
    if asignado + porcentaje > 100 + CENTAVO:
        raise ValueError(f"Con {porcentaje}% el edificio sumaría {round(asignado + porcentaje, 2)}%. "
                         f"Disponible: {round(100 - asignado, 2)}%.")


def crear_unidad(codigo, porcentaje, dni):
    """CREATE: da de alta una unidad. El piso se obtiene del código (2B → piso 2)."""
    codigo = codigo.strip().upper()
    if not utils.validar_codigo_unidad(codigo):
        raise ValueError("Código inválido. Usá piso + letra: 1A, 10B o PBA.")

    unidades = leer("unidades")
    if next((u for u in unidades if u["codigo"] == codigo), None) is not None:
        raise ValueError(f"La unidad {codigo} ya existe.")
    if buscar_propietario(dni) is None:
        raise ValueError(f"No existe un propietario con DNI {dni}. Primero dalo de alta.")
    validar_porcentaje_unidad(unidades, codigo, porcentaje)

    unidad = {
        "codigo": codigo,
        "piso": utils.piso_de_codigo(codigo),
        "porcentaje": round(porcentaje, 2),
        "dni": dni,
        "id_consorcio": ID_CONSORCIO,
    }
    unidades.append(unidad)
    guardar("unidades", unidades)
    registrar(f"Unidad creada: {codigo} ({unidad['porcentaje']}%)")
    return unidad


def modificar_unidad(codigo, porcentaje=None, dni=None):
    """UPDATE: cambia el porcentaje y/o el propietario. None = no modificar."""
    unidades = leer("unidades")
    unidad = next((u for u in unidades if u["codigo"] == codigo.strip().upper()), None)
    if unidad is None:
        raise ValueError(f"No existe la unidad {codigo}.")

    if porcentaje is not None:
        validar_porcentaje_unidad(unidades, unidad["codigo"], porcentaje)
        unidad["porcentaje"] = round(porcentaje, 2)
    if dni is not None:
        if buscar_propietario(dni) is None:
            raise ValueError(f"No existe un propietario con DNI {dni}.")
        unidad["dni"] = dni

    guardar("unidades", unidades)
    registrar(f"Unidad modificada: {unidad['codigo']}")
    return unidad


def eliminar_unidad(codigo):
    """DELETE: no se puede eliminar una unidad que ya tiene expensas (se perdería el historial)."""
    unidades = leer("unidades")
    unidad = next((u for u in unidades if u["codigo"] == codigo.strip().upper()), None)
    if unidad is None:
        raise ValueError(f"No existe la unidad {codigo}.")
    if next((e for e in leer("expensas") if e["codigo"] == unidad["codigo"]), None) is not None:
        raise ValueError(f"La unidad {unidad['codigo']} tiene expensas emitidas: no se puede eliminar.")

    unidades.remove(unidad)
    guardar("unidades", unidades)
    registrar(f"Unidad eliminada: {unidad['codigo']}")
    return unidad


# ============================================================
# GASTOS Y LIQUIDACIONES
# ============================================================

def validar_periodo(mes, anio):
    if not 1 <= mes <= 12:
        raise ValueError("El mes debe estar entre 1 y 12.")
    if not 2000 <= anio <= 2099:
        raise ValueError("El año debe estar entre 2000 y 2099.")


def cargar_gasto(mes, anio, concepto, monto, fecha):
    """
    Agrega un gasto al mes indicado. Si es el primer gasto del mes, crea la
    liquidación (abierta, con total 0). No se puede agregar a un mes ya liquidado.
    """
    validar_periodo(mes, anio)
    concepto = concepto.strip().lower()
    if concepto not in CONCEPTOS:
        raise ValueError(f"Concepto inválido. Opciones: {', '.join(CONCEPTOS)}.")
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a 0.")

    liquidaciones = leer("liquidaciones")
    liquidacion = reportes.buscar_liquidacion(liquidaciones, mes, anio)

    if liquidacion is None:
        liquidacion = {
            "id_liquidacion": utils.generar_id(liquidaciones, "id_liquidacion"),
            "mes": mes,
            "anio": anio,
            "total": 0,
            "id_consorcio": ID_CONSORCIO,
        }
        liquidaciones.append(liquidacion)
        guardar("liquidaciones", liquidaciones)
    elif reportes.esta_liquidada(liquidacion["id_liquidacion"], leer("expensas")):
        raise ValueError(f"{utils.periodo_texto(mes, anio)} ya fue liquidado: no se pueden agregar gastos.")

    gastos = leer("gastos")
    gasto = {
        "id_gasto": utils.generar_id(gastos, "id_gasto"),
        "concepto": concepto,
        "monto": round(monto, 2),
        "fecha": fecha.isoformat(),          # JSON no guarda date: se guarda 'aaaa-mm-dd'
        "id_liquidacion": liquidacion["id_liquidacion"],
    }
    gastos.append(gasto)
    guardar("gastos", gastos)
    registrar(f"Gasto cargado: {concepto} {utils.formatear_moneda(monto)} "
              f"({utils.periodo_texto(mes, anio)})")
    return gasto


def listar_gastos(mes, anio):
    """Gastos de un mes ordenados por fecha ([] si no hay liquidación)."""
    liquidacion = reportes.buscar_liquidacion(leer("liquidaciones"), mes, anio)
    if liquidacion is None:
        return []
    gastos = [g for g in leer("gastos") if g["id_liquidacion"] == liquidacion["id_liquidacion"]]
    return sorted(gastos, key=lambda g: g["fecha"])


def eliminar_gasto(id_gasto):
    """Elimina un gasto, solo si su mes todavía no fue liquidado."""
    gastos = leer("gastos")
    gasto = next((g for g in gastos if g["id_gasto"] == id_gasto), None)
    if gasto is None:
        raise ValueError(f"No existe el gasto {id_gasto}.")
    if reportes.esta_liquidada(gasto["id_liquidacion"], leer("expensas")):
        raise ValueError("Ese mes ya fue liquidado: no se pueden eliminar sus gastos.")

    gastos.remove(gasto)
    guardar("gastos", gastos)
    registrar(f"Gasto eliminado: id {id_gasto}")
    return gasto


def listar_liquidaciones():
    """Liquidaciones del más reciente al más viejo, con su estado y el total de gastos."""
    expensas = leer("expensas")
    gastos = leer("gastos")
    resultado = []
    for l in leer("liquidaciones"):
        del_mes = [g["monto"] for g in gastos if g["id_liquidacion"] == l["id_liquidacion"]]
        resultado.append({
            **l,
            "cantidad_gastos": len(del_mes),
            "total_gastos": round(sum(del_mes), 2),
            "estado": "Liquidada" if reportes.esta_liquidada(l["id_liquidacion"], expensas) else "Abierta",
        })
    return sorted(resultado, key=lambda l: (l["anio"], l["mes"]), reverse=True)


def liquidar_mes(mes, anio):
    """
    Cierra el mes: suma los gastos, reparte el total según el porcentaje de cada
    unidad y emite una expensa por unidad con vencimiento el día 10 del mes siguiente.

    Retorna una tupla (liquidacion, expensas_emitidas).
    """
    validar_periodo(mes, anio)
    periodo = utils.periodo_texto(mes, anio)
    liquidaciones = leer("liquidaciones")
    expensas = leer("expensas")

    liquidacion = reportes.buscar_liquidacion(liquidaciones, mes, anio)
    if liquidacion is None:
        raise ValueError(f"No hay gastos cargados para {periodo}.")
    if reportes.esta_liquidada(liquidacion["id_liquidacion"], expensas):
        raise ValueError(f"{periodo} ya fue liquidado.")

    gastos = [g for g in leer("gastos") if g["id_liquidacion"] == liquidacion["id_liquidacion"]]
    if not gastos:
        raise ValueError(f"No hay gastos cargados para {periodo}.")

    unidades = reportes.ordenar_unidades(leer("unidades"))
    if not unidades:
        raise ValueError("No hay unidades cargadas.")
    suma = reportes.suma_porcentajes(unidades)
    if abs(suma - 100) > CENTAVO:
        raise ValueError(f"Los porcentajes de las unidades suman {suma}% y deben sumar 100%.")

    total = round(reduce(lambda acc, g: acc + g["monto"], gastos, 0), 2)
    vencimiento = utils.calcular_vencimiento(mes, anio).isoformat()
    proximo_id = utils.generar_id(expensas, "id_expensa")

    emitidas = [
        {
            "id_expensa": proximo_id + i,
            "importe": importe,
            "vencimiento": vencimiento,
            "codigo": codigo,
            "id_liquidacion": liquidacion["id_liquidacion"],
        }
        for i, (codigo, importe) in enumerate(reportes.calcular_importes(total, unidades))
    ]

    liquidacion["total"] = total
    expensas.extend(emitidas)
    guardar("expensas", expensas)
    guardar("liquidaciones", liquidaciones)
    registrar(f"Liquidación {periodo}: total {utils.formatear_moneda(total)}, "
              f"{len(emitidas)} expensas emitidas")
    return liquidacion, emitidas


def expensas_del_mes(mes, anio, fecha_corte=None):
    """
    Expensas emitidas en un mes, con propietario, saldo y estado.
    Retorna una tupla (liquidacion, detalle).
    """
    datos = cargar_datos()
    liquidacion = reportes.buscar_liquidacion(datos["liquidaciones"], mes, anio)
    if liquidacion is None or not reportes.esta_liquidada(liquidacion["id_liquidacion"], datos["expensas"]):
        raise ValueError(f"{utils.periodo_texto(mes, anio)} todavía no fue liquidado.")
    del_mes = [e for e in datos["expensas"] if e["id_liquidacion"] == liquidacion["id_liquidacion"]]
    return liquidacion, reportes.detallar_expensas(del_mes, datos, fecha_o_hoy(fecha_corte))


# ============================================================
# PAGOS
# ============================================================

def expensas_pendientes(codigo, fecha_corte=None):
    """Expensas de una unidad que todavía tienen saldo, de la más vieja a la más nueva."""
    unidad = buscar_unidad(codigo)
    if unidad is None:
        raise ValueError(f"No existe la unidad {codigo}.")
    datos = cargar_datos()
    de_la_unidad = [e for e in datos["expensas"] if e["codigo"] == unidad["codigo"]]
    detalle = reportes.detallar_expensas(de_la_unidad, datos, fecha_o_hoy(fecha_corte))
    return [e for e in detalle if e["saldo"] >= CENTAVO]


def registrar_pago(id_expensa, monto, medio_pago, fecha):
    """
    Registra un pago (total o parcial) de una expensa.
    Retorna una tupla (pago, saldo_restante).
    """
    medio_pago = medio_pago.strip().lower()
    if medio_pago not in MEDIOS_PAGO:
        raise ValueError(f"Medio de pago inválido. Opciones: {', '.join(MEDIOS_PAGO)}.")
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a 0.")

    expensa = next((e for e in leer("expensas") if e["id_expensa"] == id_expensa), None)
    if expensa is None:
        raise ValueError(f"No existe la expensa {id_expensa}.")

    pagos = leer("pagos")
    saldo = reportes.saldo_expensa(expensa, pagos)
    if saldo < CENTAVO:
        raise ValueError(f"La expensa {id_expensa} ya está paga.")
    if monto > saldo + CENTAVO:
        raise ValueError(f"El monto supera el saldo pendiente ({utils.formatear_moneda(saldo)}).")

    pago = {
        "id_pago": utils.generar_id(pagos, "id_pago"),
        "fecha": fecha.isoformat(),
        "monto": round(monto, 2),
        "medio_pago": medio_pago,
        "id_expensa": id_expensa,
    }
    pagos.append(pago)
    guardar("pagos", pagos)
    registrar(f"Pago registrado: unidad {expensa['codigo']}, {utils.formatear_moneda(monto)} "
              f"en {medio_pago}")
    return pago, round(saldo - monto, 2)


def pagos_de_unidad(codigo):
    """Historial de pagos de una unidad, con el período de cada expensa."""
    unidad = buscar_unidad(codigo)
    if unidad is None:
        raise ValueError(f"No existe la unidad {codigo}.")

    periodo = reportes.periodos(leer("liquidaciones"))
    expensas = {e["id_expensa"]: e for e in leer("expensas") if e["codigo"] == unidad["codigo"]}

    pagos = []
    for p in leer("pagos"):
        if p["id_expensa"] in expensas:
            mes, anio = periodo[expensas[p["id_expensa"]]["id_liquidacion"]]
            pagos.append({**p, "periodo": utils.periodo_texto(mes, anio)})
    return sorted(pagos, key=lambda p: p["fecha"])


# ============================================================
# CONSULTAS Y REPORTES
# ============================================================

def tabla_anual(anio, fecha_corte=None):
    """
    Tabla anual de pagos: retorna (codigos, matriz, pagaron_por_mes).
    matriz[i][j] es el estado de la unidad codigos[i] en el mes j+1.
    """
    codigos, matriz = reportes.construir_tabla_anual(anio, cargar_datos(), fecha_o_hoy(fecha_corte))
    return codigos, matriz, reportes.pagos_por_mes(matriz)


def exportar_tabla_anual(anio, fecha_corte=None):
    """Guarda la tabla anual en data/tabla_pagos_<anio>.csv y retorna la ruta."""
    codigos, matriz, pagaron = tabla_anual(anio, fecha_corte)
    filas = [[codigos[i]] + fila for i, fila in enumerate(matriz)]
    filas.append(["Pagaron"] + pagaron)

    ruta = RUTA_DATA / f"tabla_pagos_{anio}.csv"
    if not storage.exportar_csv(ruta, ["Unidad"] + list(MESES), filas):
        raise OSError(f"No se pudo exportar {ruta.name}.")
    registrar(f"Tabla anual {anio} exportada a CSV")
    return ruta


def listar_morosos(fecha_corte=None):
    """Unidades con deuda vencida, de mayor a menor deuda (con recargo por mora)."""
    return reportes.listar_morosos(cargar_datos(), fecha_o_hoy(fecha_corte))


def ranking_deudores(cantidad=3, fecha_corte=None):
    """Los 'cantidad' mayores deudores (slicing de la lista de morosos)."""
    return listar_morosos(fecha_corte)[:cantidad]


def nivel_cobranza(fecha_corte=None):
    """Retorna (porcentaje_al_dia, codigos_al_dia, codigos_con_deuda)."""
    datos = cargar_datos()
    morosos = reportes.listar_morosos(datos, fecha_o_hoy(fecha_corte))
    return reportes.porcentaje_al_dia(datos, morosos)


def recaudacion_del_mes(mes, anio):
    """Lo cobrado frente a lo liquidado en un mes. Retorna (liquidacion, resumen)."""
    datos = cargar_datos()
    liquidacion = reportes.buscar_liquidacion(datos["liquidaciones"], mes, anio)
    if liquidacion is None or not reportes.esta_liquidada(liquidacion["id_liquidacion"], datos["expensas"]):
        raise ValueError(f"{utils.periodo_texto(mes, anio)} todavía no fue liquidado.")
    return liquidacion, reportes.recaudacion(liquidacion, datos)


def gastos_por_categoria(anio, mes=None):
    """Gastos por concepto de un año completo o de un mes. Retorna (totales, total)."""
    ids = {l["id_liquidacion"] for l in leer("liquidaciones")
           if l["anio"] == anio and (mes is None or l["mes"] == mes)}
    gastos = [g for g in leer("gastos") if g["id_liquidacion"] in ids]
    return reportes.gastos_por_categoria(gastos)
