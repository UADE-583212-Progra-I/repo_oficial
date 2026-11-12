"""
constantes.py — Valores fijos del sistema.

Son tuplas y constantes que no cambian durante la ejecución:
catálogos (meses, conceptos de gasto, medios de pago) y reglas de negocio
(día de vencimiento, recargo por mora).
"""

# ── Consorcio que administra el programa ─────────────────────────
ID_CONSORCIO = 1

# ── Catálogos (tuplas: inmutables) ───────────────────────────────
MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")

CONCEPTOS = ("limpieza", "luz", "ascensor", "mantenimiento")

MEDIOS_PAGO = ("efectivo", "transferencia", "débito", "crédito")

# ── Reglas de negocio ────────────────────────────────────────────
DIA_VENCIMIENTO = 10      # la expensa vence el día 10 del mes siguiente
RECARGO_MENSUAL = 0.03    # 3 % del saldo por cada mes (o fracción) de atraso
CENTAVO = 0.01            # tolerancia para comparar montos con decimales

# ── Estados de una expensa en la tabla anual de pagos ────────────
ESTADO_PAGO = "Pagó"
ESTADO_DEUDA = "Debe"
ESTADO_PENDIENTE = "Pendiente"   # todavía no venció
SIN_EXPENSA = "-"                # ese mes no se liquidó

# ── Interfaz ─────────────────────────────────────────────────────
MAX_INTENTOS = 3      # intentos para ingresar un dato válido
TAMANIO_PAGINA = 5    # registros por página en los listados
