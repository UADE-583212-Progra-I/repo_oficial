"""
menus.py — Menús y flujos de la aplicación.

Cada flujo coordina, no calcula:
  1. pide los datos con interface,
  2. llama a services,
  3. muestra el resultado con interface.

Los errores de negocio (ValueError) y de archivos (OSError) se atrapan en
ejecutar_menu(): se muestra el mensaje y el menú sigue funcionando.
"""
from src import interface, services, utils
from src.constantes import CONCEPTOS, MEDIOS_PAGO


def ejecutar_menu(titulo, opciones, texto_salida="Volver"):
    """
    Muestra un menú y ejecuta la opción elegida hasta que el usuario elija 0.
    opciones: lista de tuplas (texto, funcion).
    """
    while True:
        interface.mostrar_menu(titulo, [texto for texto, _ in opciones], texto_salida)
        opcion = interface.pedir_opcion_menu(len(opciones))
        if opcion is None:
            interface.mostrar_error("Opción inválida. Ingresá un número del menú.")
            continue
        if opcion == 0:
            return

        _, funcion = opciones[opcion - 1]
        try:
            funcion()
        except (ValueError, OSError) as e:
            interface.mostrar_error(e)
        except EOFError:
            raise                      # se cerró la entrada: lo maneja menu_principal()
        except Exception as e:         # red de seguridad en el nivel más alto
            services.registrar(f"Error inesperado: {type(e).__name__}: {e}")
            interface.mostrar_error(f"Ocurrió un error inesperado ({type(e).__name__}): {e}")


# ============================================================
# PROPIETARIOS
# ============================================================

def flujo_listar_propietarios():
    interface.mostrar_paginado(services.listar_propietarios(), interface.mostrar_propietarios)


def flujo_buscar_propietario():
    dni = interface.pedir_dni()
    propietario = services.buscar_propietario(dni)
    if propietario is None:
        interface.mostrar_warning(f"No existe un propietario con DNI {dni}.")
        return
    interface.mostrar_propietarios([propietario])
    codigos = services.unidades_de_propietario(dni)
    interface.mostrar_mensaje(f"Unidades: {', '.join(codigos) if codigos else 'ninguna'}")


def flujo_buscar_propietario_por_nombre():
    texto = interface.pedir_texto("Nombre o parte del nombre: ")
    interface.mostrar_propietarios(services.buscar_propietarios_por_nombre(texto))


def flujo_crear_propietario():
    interface.mostrar_subtitulo("Nuevo propietario")
    dni = interface.pedir_dni()
    if services.buscar_propietario(dni) is not None:
        raise ValueError(f"Ya existe un propietario con DNI {dni}.")
    nombre = interface.pedir_nombre()
    telefono = interface.pedir_telefono()
    email = interface.pedir_email()
    propietario = services.crear_propietario(dni, nombre, telefono, email)
    interface.mostrar_ok(f"Propietario {propietario['nombre']} creado.")


def flujo_modificar_propietario():
    dni = interface.pedir_dni()
    propietario = services.buscar_propietario(dni)
    if propietario is None:
        raise ValueError(f"No existe un propietario con DNI {dni}.")
    interface.mostrar_propietarios([propietario])
    interface.mostrar_mensaje("Dejá vacío (Enter) lo que no quieras cambiar.")
    nombre = interface.pedir_opcional("Nuevo nombre: ", utils.validar_nombre, "Solo letras y espacios.")
    telefono = interface.pedir_opcional("Nuevo teléfono: ", utils.validar_telefono, "Entre 8 y 13 dígitos.")
    email = interface.pedir_opcional("Nuevo email: ", utils.validar_email, "Email inválido.")
    actualizado = services.modificar_propietario(dni, nombre, telefono, email)
    interface.mostrar_ok("Propietario actualizado.")
    interface.mostrar_propietarios([actualizado])


def flujo_eliminar_propietario():
    dni = interface.pedir_dni()
    propietario = services.buscar_propietario(dni)
    if propietario is None:
        raise ValueError(f"No existe un propietario con DNI {dni}.")
    if interface.confirmar(f"¿Eliminar a {propietario['nombre']}?"):
        services.eliminar_propietario(dni)
        interface.mostrar_ok("Propietario eliminado.")


def menu_propietarios():
    ejecutar_menu("Propietarios", [
        ("Ver todos", flujo_listar_propietarios),
        ("Buscar por DNI", flujo_buscar_propietario),
        ("Buscar por nombre", flujo_buscar_propietario_por_nombre),
        ("Crear propietario", flujo_crear_propietario),
        ("Modificar propietario", flujo_modificar_propietario),
        ("Eliminar propietario", flujo_eliminar_propietario),
    ])


# ============================================================
# UNIDADES
# ============================================================

def flujo_listar_unidades():
    interface.mostrar_unidades(services.listar_unidades())


def flujo_crear_unidad():
    interface.mostrar_subtitulo("Nueva unidad")
    disponible = services.porcentaje_disponible()
    if disponible <= 0:
        raise ValueError("El edificio ya tiene asignado el 100%. Primero bajá el porcentaje de otra unidad.")
    interface.mostrar_mensaje(f"Porcentaje disponible del edificio: {utils.formatear_porcentaje(disponible, 2)}")
    codigo = interface.pedir_codigo_unidad()
    if services.buscar_unidad(codigo) is not None:
        raise ValueError(f"La unidad {codigo} ya existe.")
    porcentaje = interface.pedir_porcentaje()
    dni = interface.pedir_dni("DNI del propietario: ")
    unidad = services.crear_unidad(codigo, porcentaje, dni)
    interface.mostrar_ok(f"Unidad {unidad['codigo']} creada (piso {unidad['piso']}, {unidad['porcentaje']}%).")


def flujo_modificar_unidad():
    codigo = interface.pedir_codigo_unidad()
    unidad = services.buscar_unidad(codigo)
    if unidad is None:
        raise ValueError(f"No existe la unidad {codigo}.")
    interface.mostrar_mensaje(f"Actual: {unidad['porcentaje']}%, propietario DNI {unidad['dni']}.")
    interface.mostrar_mensaje("Disponible para esta unidad: "
                              f"{utils.formatear_porcentaje(services.porcentaje_disponible(codigo), 2)}")
    interface.mostrar_mensaje("Dejá vacío (Enter) lo que no quieras cambiar.")
    porcentaje = interface.pedir_opcional("Nuevo porcentaje: ", utils.validar_porcentaje, "Mayor a 0 y hasta 100.")
    dni = interface.pedir_opcional("DNI del nuevo propietario: ", utils.validar_dni, "7 u 8 dígitos.")
    services.modificar_unidad(
        codigo,
        porcentaje=utils.convertir_decimal(porcentaje) if porcentaje else None,
        dni=int(dni) if dni else None,
    )
    interface.mostrar_ok(f"Unidad {codigo} actualizada.")


def flujo_eliminar_unidad():
    codigo = interface.pedir_codigo_unidad()
    if services.buscar_unidad(codigo) is None:
        raise ValueError(f"No existe la unidad {codigo}.")
    if interface.confirmar(f"¿Eliminar la unidad {codigo}?"):
        services.eliminar_unidad(codigo)
        interface.mostrar_ok(f"Unidad {codigo} eliminada.")


def menu_unidades():
    ejecutar_menu("Unidades", [
        ("Ver todas", flujo_listar_unidades),
        ("Crear unidad", flujo_crear_unidad),
        ("Modificar unidad", flujo_modificar_unidad),
        ("Eliminar unidad", flujo_eliminar_unidad),
    ])


# ============================================================
# GASTOS Y LIQUIDACIONES
# ============================================================

def flujo_cargar_gasto():
    interface.mostrar_subtitulo("Cargar gasto")
    mes, anio = interface.pedir_periodo()
    concepto = interface.pedir_opcion_lista("Concepto:", CONCEPTOS)
    monto = interface.pedir_monto()
    fecha = interface.pedir_fecha()
    gasto = services.cargar_gasto(mes, anio, concepto, monto, fecha)
    interface.mostrar_ok(f"Gasto #{gasto['id_gasto']} cargado.")


def flujo_ver_gastos():
    mes, anio = interface.pedir_periodo()
    interface.mostrar_gastos(services.listar_gastos(mes, anio), f"Gastos {utils.periodo_texto(mes, anio)}")


def flujo_eliminar_gasto():
    id_gasto = interface.pedir_entero("ID del gasto a eliminar ", 0)
    if id_gasto and interface.confirmar(f"¿Eliminar el gasto #{id_gasto}?"):
        services.eliminar_gasto(id_gasto)
        interface.mostrar_ok("Gasto eliminado.")


def flujo_ver_liquidaciones():
    interface.mostrar_liquidaciones(services.listar_liquidaciones())


def flujo_liquidar_mes():
    interface.mostrar_subtitulo("Liquidar mes")
    mes, anio = interface.pedir_periodo()
    gastos = services.listar_gastos(mes, anio)
    interface.mostrar_gastos(gastos, f"Gastos {utils.periodo_texto(mes, anio)}")
    if not gastos:
        return
    if interface.confirmar("Una vez liquidado no se pueden agregar gastos. ¿Liquidar?"):
        services.liquidar_mes(mes, anio)
        liquidacion, detalle = services.expensas_del_mes(mes, anio)
        interface.mostrar_ok("Mes liquidado. Expensas emitidas:")
        interface.mostrar_expensas(liquidacion, detalle)


def flujo_ver_expensas():
    mes, anio = interface.pedir_periodo()
    liquidacion, detalle = services.expensas_del_mes(mes, anio)
    interface.mostrar_expensas(liquidacion, detalle)


def menu_gastos():
    ejecutar_menu("Gastos y liquidaciones", [
        ("Cargar gasto", flujo_cargar_gasto),
        ("Ver gastos de un mes", flujo_ver_gastos),
        ("Eliminar gasto", flujo_eliminar_gasto),
        ("Ver liquidaciones", flujo_ver_liquidaciones),
        ("Liquidar mes y emitir expensas", flujo_liquidar_mes),
        ("Ver expensas de un mes", flujo_ver_expensas),
    ])


# ============================================================
# PAGOS
# ============================================================

def flujo_registrar_pago():
    interface.mostrar_subtitulo("Registrar pago")
    codigo = interface.pedir_codigo_unidad()
    pendientes = services.expensas_pendientes(codigo)
    if not pendientes:
        interface.mostrar_ok(f"La unidad {codigo} no tiene expensas pendientes.")
        return
    interface.mostrar_expensas_pendientes(pendientes)

    ids = [e["id_expensa"] for e in pendientes]
    id_expensa = int(interface.pedir_dato("ID de la expensa a pagar: ",
                                          lambda v: v.isdigit() and int(v) in ids,
                                          "Elegí un ID de la tabla."))
    expensa = next(e for e in pendientes if e["id_expensa"] == id_expensa)

    monto = interface.pedir_monto("Monto ", por_defecto=expensa["saldo"])
    medio = interface.pedir_opcion_lista("Medio de pago:", MEDIOS_PAGO)
    fecha = interface.pedir_fecha()
    pago, saldo = services.registrar_pago(id_expensa, monto, medio, fecha)

    interface.mostrar_ok(f"Pago #{pago['id_pago']} registrado.")
    if saldo > 0:
        interface.mostrar_warning(f"La expensa queda con un saldo de {utils.formatear_moneda(saldo)}.")


def flujo_ver_pagos_unidad():
    codigo = interface.pedir_codigo_unidad()
    interface.mostrar_pagos(services.pagos_de_unidad(codigo))


def flujo_ver_pendientes_unidad():
    codigo = interface.pedir_codigo_unidad()
    pendientes = services.expensas_pendientes(codigo)
    if not pendientes:
        interface.mostrar_ok(f"La unidad {codigo} está al día.")
        return
    interface.mostrar_expensas_pendientes(pendientes)


def menu_pagos():
    ejecutar_menu("Pagos", [
        ("Registrar pago", flujo_registrar_pago),
        ("Ver expensas pendientes de una unidad", flujo_ver_pendientes_unidad),
        ("Ver pagos de una unidad", flujo_ver_pagos_unidad),
    ])


# ============================================================
# REPORTES
# ============================================================

def flujo_tabla_anual():
    anio = interface.pedir_anio()
    codigos, matriz, pagaron = services.tabla_anual(anio)
    interface.mostrar_tabla_anual(anio, codigos, matriz, pagaron)
    if matriz and interface.confirmar("¿Exportar la tabla a CSV?"):
        ruta = services.exportar_tabla_anual(anio)
        interface.mostrar_ok(f"Tabla exportada en {ruta}")


def flujo_morosos():
    interface.mostrar_morosos(services.listar_morosos())


def flujo_recaudacion():
    mes, anio = interface.pedir_periodo()
    liquidacion, resumen = services.recaudacion_del_mes(mes, anio)
    interface.mostrar_recaudacion(liquidacion, resumen)


def flujo_nivel_cobranza():
    porcentaje, al_dia, con_deuda = services.nivel_cobranza()
    interface.mostrar_nivel_cobranza(porcentaje, al_dia, con_deuda)


def flujo_ranking():
    cantidad = interface.pedir_entero("¿Cuántos deudores mostrar? ", 3)
    interface.mostrar_ranking(services.ranking_deudores(cantidad))


def flujo_gastos_por_categoria():
    anio = interface.pedir_anio()
    mes = interface.pedir_opcional("Mes (1 a 12) [Enter = año completo]: ", utils.validar_mes,
                                   "El mes debe ser un número del 1 al 12.")
    if mes:
        titulo = f"Gastos por categoría {utils.periodo_texto(int(mes), anio)}"
        totales, total = services.gastos_por_categoria(anio, int(mes))
    else:
        titulo = f"Gastos por categoría {anio}"
        totales, total = services.gastos_por_categoria(anio)
    interface.mostrar_gastos_por_categoria(titulo, totales, total)


def menu_reportes():
    ejecutar_menu("Consultas y reportes", [
        ("Tabla anual de pagos", flujo_tabla_anual),
        ("Morosos", flujo_morosos),
        ("Recaudación del mes", flujo_recaudacion),
        ("Porcentaje del edificio al día", flujo_nivel_cobranza),
        ("Ranking de deudores", flujo_ranking),
        ("Gastos por categoría", flujo_gastos_por_categoria),
    ])


# ============================================================
# CONSORCIO
# ============================================================

def flujo_ver_consorcio():
    interface.mostrar_consorcio(services.obtener_consorcio())


def flujo_modificar_consorcio():
    interface.mostrar_mensaje("Dejá vacío (Enter) lo que no quieras cambiar.")
    nombre = interface.pedir_opcional("Nombre: ", lambda v: True, "")
    direccion = interface.pedir_opcional("Dirección: ", lambda v: True, "")
    cuit = interface.pedir_opcional("CUIT (30-12345678-9): ", utils.validar_cuit, "Formato: 30-12345678-9.")
    interface.mostrar_consorcio(services.modificar_consorcio(nombre, direccion, cuit))
    interface.mostrar_ok("Datos actualizados.")


def menu_consorcio():
    ejecutar_menu("Datos del consorcio", [
        ("Ver datos", flujo_ver_consorcio),
        ("Modificar datos", flujo_modificar_consorcio),
    ])


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu_principal():
    consorcio = services.obtener_consorcio()
    nombre = consorcio["nombre"] if consorcio else "sin datos"
    try:
        ejecutar_menu(f"Gestor de Consorcio — {nombre}", [
            ("Propietarios", menu_propietarios),
            ("Unidades", menu_unidades),
            ("Gastos y liquidaciones", menu_gastos),
            ("Pagos", menu_pagos),
            ("Consultas y reportes", menu_reportes),
            ("Datos del consorcio", menu_consorcio),
        ], texto_salida="Salir")
    except (KeyboardInterrupt, EOFError):
        print()
    interface.mostrar_mensaje("¡Hasta luego!")
