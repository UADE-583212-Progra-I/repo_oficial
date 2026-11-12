"""
interface.py — Todo lo que el usuario ve y escribe: input(), print() y tablas.

- Las funciones pedir_* leen un dato, validan su FORMATO con utils y
  lo devuelven ya convertido (int, float, date...).
- Las funciones mostrar_* reciben datos ya calculados y los imprimen.
No contiene reglas de negocio: eso vive en services.py y reportes.py.
"""
from datetime import date

from tabulate import tabulate

from src import utils
from src.constantes import MAX_INTENTOS, MESES, RECARGO_MENSUAL, TAMANIO_PAGINA

FORMATO_TABLA = "grid"


# ============================================================
# MENSAJES
# ============================================================

def mostrar_titulo(texto):
    print("\n" + "=" * 50)
    print(f"  {texto}")
    print("=" * 50)


def mostrar_subtitulo(texto):
    print(f"\n--- {texto} ---")


def mostrar_mensaje(mensaje):
    print(mensaje)


def mostrar_ok(mensaje):
    print(f"OK: {mensaje}")


def mostrar_warning(mensaje):
    print(f"ATENCIÓN: {mensaje}")


def mostrar_error(mensaje):
    print(f"ERROR: {mensaje}")


def mostrar_tabla(filas, encabezados):
    print(tabulate(filas, headers=encabezados, tablefmt=FORMATO_TABLA))


def mostrar_menu(titulo, textos, texto_salida="Volver"):
    mostrar_titulo(titulo)
    for numero, texto in enumerate(textos, 1):
        print(f"  {numero}. {texto}")
    print(f"  0. {texto_salida}")


def pedir_opcion_menu(cantidad):
    """Retorna el número elegido (0 a cantidad) o None si no es una opción válida."""
    opcion = input("\nOpción: ").strip()
    if opcion.isdigit() and int(opcion) <= cantidad:
        return int(opcion)
    return None


# ============================================================
# LECTURA DE DATOS
# ============================================================

def pedir_dato(mensaje, validador, error):
    """
    Pide un dato hasta que cumpla el validador.
    Si se agotan los MAX_INTENTOS lanza ValueError y se cancela la operación
    (el else del for se ejecuta solo si el bucle terminó sin return).
    """
    for intento in range(1, MAX_INTENTOS + 1):
        valor = input(mensaje).strip()
        if validador(valor):
            return valor
        mostrar_error(f"{error} (intento {intento} de {MAX_INTENTOS})")
    else:
        raise ValueError("Se superó el máximo de intentos. Operación cancelada.")


def pedir_opcional(mensaje, validador, error):
    """Igual que pedir_dato, pero Enter (vacío) también es válido: significa 'no cambiar'."""
    return pedir_dato(mensaje, lambda valor: valor == "" or validador(valor), error)


def pedir_texto(mensaje):
    return pedir_dato(mensaje, lambda valor: valor != "", "El dato no puede estar vacío.")


def pedir_dni(mensaje="DNI (sin puntos): "):
    return int(pedir_dato(mensaje, utils.validar_dni, "El DNI debe tener 7 u 8 dígitos, sin puntos."))


def pedir_nombre(mensaje="Nombre y apellido: "):
    return pedir_dato(mensaje, utils.validar_nombre, "Solo se permiten letras y espacios.")


def pedir_telefono(mensaje="Teléfono: "):
    return pedir_dato(mensaje, utils.validar_telefono, "El teléfono debe tener entre 8 y 13 dígitos.")


def pedir_email(mensaje="Email: "):
    return pedir_dato(mensaje, utils.validar_email, "Email inválido (ej: nombre@mail.com).")


def pedir_codigo_unidad(mensaje="Código de la unidad (ej: 1A, 10B, PBA): "):
    return pedir_dato(mensaje, utils.validar_codigo_unidad, "Usá piso + letra: 1A, 10B o PBA.").upper()


def pedir_porcentaje(mensaje="Porcentaje (ej: 15 o 12.5): "):
    valor = pedir_dato(mensaje, utils.validar_porcentaje, "Ingresá un número mayor a 0 y hasta 100.")
    return utils.convertir_decimal(valor)


def pedir_monto(mensaje="Monto: ", por_defecto=None):
    """Pide un importe. Si hay un valor por defecto, Enter lo acepta."""
    error = "Ingresá un importe mayor a 0, sin separador de miles (ej: 150000 o 150000,50)."
    if por_defecto is None:
        return utils.convertir_decimal(pedir_dato(mensaje, utils.validar_monto, error))
    valor = pedir_opcional(f"{mensaje}[Enter = {utils.formatear_moneda(por_defecto)}]: ",
                           utils.validar_monto, error)
    return por_defecto if valor == "" else utils.convertir_decimal(valor)


def pedir_mes(mensaje="Mes (1 a 12): "):
    return int(pedir_dato(mensaje, utils.validar_mes, "El mes debe ser un número del 1 al 12."))


def pedir_anio(mensaje="Año [Enter = año actual]: "):
    valor = pedir_opcional(mensaje, utils.validar_anio, "Año inválido (ej: 2026).")
    return date.today().year if valor == "" else int(valor)


def pedir_periodo():
    """Retorna una tupla (mes, anio)."""
    return pedir_mes(), pedir_anio()


def pedir_fecha(mensaje="Fecha dd/mm/aaaa [Enter = hoy]: "):
    valor = pedir_opcional(mensaje, utils.validar_fecha, "Fecha inválida. Usá el formato dd/mm/aaaa.")
    return date.today() if valor == "" else utils.texto_a_fecha(valor)


def pedir_entero(mensaje, por_defecto):
    valor = pedir_opcional(f"{mensaje}[Enter = {por_defecto}]: ",
                           utils.validar_entero_positivo, "Ingresá un número entero mayor a 0.")
    return por_defecto if valor == "" else int(valor)


def pedir_opcion_lista(titulo, opciones):
    """Muestra una lista numerada (tupla de opciones) y retorna el elemento elegido."""
    print(titulo)
    for numero, opcion in enumerate(opciones, 1):
        print(f"  {numero}. {opcion.capitalize()}")
    valor = pedir_dato("Opción: ",
                       lambda v: v.isdigit() and 1 <= int(v) <= len(opciones),
                       f"Elegí un número del 1 al {len(opciones)}.")
    return opciones[int(valor) - 1]


def confirmar(mensaje):
    return input(f"{mensaje} (s/n): ").strip().lower() in ("s", "si", "sí")


def mostrar_paginado(registros, funcion_mostrar):
    """Muestra una lista de a TAMANIO_PAGINA registros por vez (slicing)."""
    paginas = utils.total_paginas(len(registros), TAMANIO_PAGINA)
    for pagina in range(1, paginas + 1):
        funcion_mostrar(utils.paginar(registros, pagina, TAMANIO_PAGINA))
        if pagina < paginas:
            respuesta = input(f"Página {pagina} de {paginas}. Enter para seguir, 0 para salir: ")
            if respuesta.strip() == "0":
                break


# ============================================================
# CONSORCIO, PROPIETARIOS Y UNIDADES
# ============================================================

def mostrar_consorcio(consorcio):
    if consorcio is None:
        mostrar_warning("Todavía no se cargaron los datos del consorcio.")
        return
    mostrar_tabla([[consorcio["nombre"], consorcio["direccion"], consorcio["cuit"]]],
                  ["Nombre", "Dirección", "CUIT"])


def mostrar_propietarios(propietarios):
    if not propietarios:
        mostrar_warning("No hay propietarios para mostrar.")
        return
    filas = [[p["dni"], p["nombre"], p["telefono"], p["email"]] for p in propietarios]
    mostrar_tabla(filas, ["DNI", "Nombre", "Teléfono", "Email"])


def texto_piso(piso):
    return "PB" if piso == 0 else piso


def mostrar_unidades(unidades):
    if not unidades:
        mostrar_warning("No hay unidades cargadas.")
        return
    filas = [[u["codigo"], texto_piso(u["piso"]), utils.formatear_porcentaje(u["porcentaje"], 2), u["propietario"], u["dni"]]
             for u in unidades]
    total = sum([u["porcentaje"] for u in unidades])
    filas.append(["TOTAL", "", utils.formatear_porcentaje(total, 2), "", ""])
    mostrar_tabla(filas, ["Unidad", "Piso", "Porcentaje", "Propietario", "DNI"])


# ============================================================
# GASTOS, LIQUIDACIONES Y EXPENSAS
# ============================================================

def mostrar_gastos(gastos, titulo):
    mostrar_subtitulo(titulo)
    if not gastos:
        mostrar_warning("No hay gastos cargados.")
        return
    filas = [[g["id_gasto"], utils.fecha_a_texto(g["fecha"]), g["concepto"].capitalize(),
              utils.formatear_moneda(g["monto"])] for g in gastos]
    filas.append(["", "", "TOTAL", utils.formatear_moneda(sum([g["monto"] for g in gastos]))])
    mostrar_tabla(filas, ["ID", "Fecha", "Concepto", "Monto"])


def mostrar_liquidaciones(liquidaciones):
    if not liquidaciones:
        mostrar_warning("No hay liquidaciones.")
        return
    filas = [[l["id_liquidacion"], utils.periodo_texto(l["mes"], l["anio"]), l["cantidad_gastos"],
              utils.formatear_moneda(l["total_gastos"]), l["estado"]] for l in liquidaciones]
    mostrar_tabla(filas, ["ID", "Período", "Gastos", "Total gastos", "Estado"])


def mostrar_expensas(liquidacion, detalle):
    """Emisión de expensas: importe y vencimiento de cada unidad."""
    mostrar_subtitulo(f"Expensas {utils.periodo_texto(liquidacion['mes'], liquidacion['anio'])} "
                      f"— total liquidado {utils.formatear_moneda(liquidacion['total'])}")
    filas = [[e["codigo"], e["propietario"], utils.formatear_porcentaje(e["porcentaje"], 2),
              utils.formatear_moneda(e["importe"]), utils.fecha_a_texto(e["vencimiento"]),
              utils.formatear_moneda(e["pagado"]), utils.formatear_moneda(e["saldo"]), e["estado"]]
             for e in detalle]
    mostrar_tabla(filas, ["Unidad", "Propietario", "%", "Importe", "Vence", "Pagado", "Saldo", "Estado"])


def mostrar_expensas_pendientes(pendientes):
    filas = [[e["id_expensa"], utils.periodo_texto(e["mes"], e["anio"]),
              utils.formatear_moneda(e["importe"]), utils.formatear_moneda(e["saldo"]),
              utils.fecha_a_texto(e["vencimiento"]), e["estado"]] for e in pendientes]
    mostrar_tabla(filas, ["ID", "Período", "Importe", "Saldo", "Vence", "Estado"])


def mostrar_pagos(pagos):
    if not pagos:
        mostrar_warning("No hay pagos registrados.")
        return
    filas = [[p["id_pago"], utils.fecha_a_texto(p["fecha"]), p["periodo"],
              p["medio_pago"].capitalize(), utils.formatear_moneda(p["monto"])] for p in pagos]
    mostrar_tabla(filas, ["ID", "Fecha", "Expensa", "Medio", "Monto"])


# ============================================================
# REPORTES
# ============================================================

def mostrar_tabla_anual(anio, codigos, matriz, pagaron):
    mostrar_subtitulo(f"Tabla anual de pagos {anio}")
    if not matriz:
        mostrar_warning("No hay unidades cargadas.")
        return
    filas = [[codigos[i]] + fila for i, fila in enumerate(matriz)]
    filas.append(["Pagaron"] + pagaron)
    mostrar_tabla(filas, ["Unidad"] + list(MESES))
    mostrar_mensaje("Pagó = sin saldo · Debe = vencida con saldo · Pendiente = aún no vence · - = sin liquidar")


def texto_meses(meses):
    """[(4, 2026), (5, 2026)] → 'Abr 2026, May 2026'."""
    return ", ".join([utils.periodo_texto(mes, anio) for mes, anio in meses])


def mostrar_morosos(morosos):
    mostrar_subtitulo("Morosos")
    if not morosos:
        mostrar_ok("No hay deudas vencidas. ¡Todo el edificio está al día!")
        return
    filas = [[m["codigo"], m["propietario"], texto_meses(m["meses"]), len(m["meses"]),
              utils.formatear_moneda(m["saldo"]), utils.formatear_moneda(m["recargo"]),
              utils.formatear_moneda(m["total"])] for m in morosos]
    total = sum([m["total"] for m in morosos])
    filas.append(["", "", "", "", "", "TOTAL", utils.formatear_moneda(total)])
    mostrar_tabla(filas, ["Unidad", "Propietario", "Meses adeudados", "Cant.", "Saldo", "Recargo", "Total"])
    mostrar_mensaje(f"Recargo por mora: {utils.formatear_porcentaje(RECARGO_MENSUAL * 100, 0)} mensual sobre el saldo de cada expensa.")


def mostrar_ranking(ranking):
    mostrar_subtitulo("Ranking de deudores")
    if not ranking:
        mostrar_ok("No hay deudores.")
        return
    filas = [[posicion, m["codigo"], m["propietario"], utils.formatear_moneda(m["total"]),
              utils.periodo_texto(*m["meses"][0]), m["atraso"]]
             for posicion, m in enumerate(ranking, 1)]
    mostrar_tabla(filas, ["#", "Unidad", "Propietario", "Deuda total", "Debe desde", "Meses de atraso"])


def mostrar_recaudacion(liquidacion, resumen):
    mostrar_subtitulo(f"Recaudación {utils.periodo_texto(liquidacion['mes'], liquidacion['anio'])}")
    filas = [
        ["Liquidado", utils.formatear_moneda(resumen["liquidado"])],
        ["Cobrado", utils.formatear_moneda(resumen["cobrado"])],
        ["Pendiente", utils.formatear_moneda(resumen["pendiente"])],
        ["% cobrado", utils.formatear_porcentaje(resumen["porcentaje"])],
    ]
    mostrar_tabla(filas, ["Concepto", "Importe"])
    por_medio = [[medio.capitalize(), utils.formatear_moneda(monto)]
                 for medio, monto in resumen["por_medio"].items() if monto > 0]
    if por_medio:
        mostrar_tabla(por_medio, ["Medio de pago", "Cobrado"])


def mostrar_nivel_cobranza(porcentaje, al_dia, con_deuda):
    mostrar_subtitulo("Nivel de cobranza")
    total = len(al_dia) + len(con_deuda)
    mostrar_mensaje(f"Unidades al día: {utils.formatear_porcentaje(porcentaje)} ({len(al_dia)} de {total})")
    mostrar_mensaje(f"  Al día:    {', '.join(al_dia) if al_dia else '-'}")
    mostrar_mensaje(f"  Con deuda: {', '.join(con_deuda) if con_deuda else '-'}")


def mostrar_gastos_por_categoria(titulo, totales, total):
    mostrar_subtitulo(titulo)
    if total == 0:
        mostrar_warning("No hay gastos en ese período.")
        return
    ordenados = sorted(totales.items(), key=lambda item: item[1], reverse=True)
    filas = [[concepto.capitalize(), utils.formatear_moneda(monto), utils.formatear_porcentaje(monto / total * 100)]
             for concepto, monto in ordenados]
    filas.append(["TOTAL", utils.formatear_moneda(total), utils.formatear_porcentaje(100)])
    mostrar_tabla(filas, ["Concepto", "Monto", "% del total"])
