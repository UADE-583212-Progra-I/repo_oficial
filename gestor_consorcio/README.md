# Gestor de Consorcio

TPO de Programación I (UADE, curso 583212).

## Tema

Gestión de expensas de un consorcio.

## Integrantes

- Joaquín Benz
- Franco Arias
- Luca Czernuczka

## Descripción

Es un programa en Python para el administrador de un edificio. Permite cargar los gastos del mes, repartirlos entre los departamentos según el porcentaje de cada uno y registrar los pagos de los vecinos. Hoy la boleta de expensas se arma a mano, los pagos quedan anotados en distintos lugares y calcular quién debe lleva horas. Con el sistema eso sale en segundos.

## Funcionalidades

**Gestión de datos**
- CRUD de propietarios (alta, listado paginado, búsqueda por DNI y por nombre, modificación y baja)
- CRUD de unidades (departamento, piso, porcentaje y propietario)
- Carga de gastos del mes (limpieza, luz, ascensor, mantenimiento)

**Liquidación y pagos**
- Liquidación mensual: reparte el total de gastos entre las unidades según su porcentaje
- Emisión de expensas con importe y vencimiento por unidad
- Registro de pagos (fecha, monto y medio de pago), totales o parciales

**Consultas y reportes**
- Tabla anual de pagos: departamentos por mes, pagó o debe (exportable a CSV)
- Morosos: meses adeudados, deuda con recargo por mora y lista ordenada de mayor a menor
- Recaudación del mes
- Porcentaje del edificio que está al día
- Ranking de deudores
- Gastos por categoría

## Cómo ejecutarlo

Requiere Python 3.10 o superior (usa `match`/`case`).

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
python main.py
```

El proyecto trae datos de ejemplo del *Edificio Las Heras*: 6 unidades, 5 propietarios y las liquidaciones de enero a octubre de 2026, con algunos vecinos que deben.

## Pruebas unitarias

```bash
python -m pytest -v
```

| Archivo | Qué prueba |
|---|---|
| `test/test_utils.py` | Validaciones con regex, conversiones, fechas, paginación y matrices (`@pytest.mark.parametrize`) |
| `test/test_reportes.py` | Cálculos puros: reparto de expensas, saldos, tabla anual, morosos, recargos y reportes |
| `test/test_services.py` | Reglas de negocio con *mocking* de `storage` (no se toca el disco) |

El workflow `.github/workflows/ci.yml` corre las pruebas en GitHub Actions en cada push a `main` y `develop`.

## Estructura del proyecto

```
gestor_consorcio/
├── main.py               ← punto de entrada: python main.py
├── src/
│   ├── menus.py          ← menús y flujos (coordina, no calcula)
│   ├── interface.py      ← input() / print() / tablas con tabulate
│   ├── services.py       ← reglas de negocio y CRUD
│   ├── reportes.py       ← cálculos puros (matriz de pagos, morosos, recaudación)
│   ├── storage.py        ← único módulo que toca el disco (JSON, TXT, CSV)
│   ├── utils.py          ← validaciones con regex, conversiones y matrices
│   └── constantes.py     ← catálogos y reglas fijas (tuplas y constantes)
├── data/                 ← un JSON por entidad (las "tablas")
└── test/                 ← pruebas con pytest
```

Las dependencias van de afuera hacia adentro: `menus` → `interface` y `services` → `reportes`, `storage` y `utils`. `services` nunca usa `input()` ni `print()`, y `storage` es el único que abre archivos.

## Modelo de datos

- **Consorcio**: id_consorcio, nombre, dirección, CUIT
- **Propietario**: dni, nombre, teléfono, email
- **Unidad**: código, piso, porcentaje, dni, id_consorcio
- **Liquidación**: id_liquidación, mes, año, total, id_consorcio
- **Gasto**: id_gasto, concepto, monto, fecha, id_liquidación
- **Expensa**: id_expensa, importe, vencimiento, código, id_liquidación
- **Pago**: id_pago, fecha, monto, medio de pago, id_expensa

Un consorcio tiene muchas unidades y liquidaciones. Un propietario puede tener varias unidades. Cada liquidación agrupa los gastos del mes y genera una expensa por unidad, y cada expensa puede tener uno o más pagos.

En los JSON las claves van sin tildes ni espacios (`anio`, `direccion`, `medio_pago`, `id_liquidacion`) y las fechas se guardan como texto `aaaa-mm-dd`.

## Reglas de negocio

| Regla | Detalle |
|---|---|
| Porcentajes | La suma de las unidades no puede pasar el 100 %, y para liquidar tiene que dar exactamente 100 % |
| Liquidación | Se crea con el primer gasto del mes. Al liquidar se emite una expensa por unidad y el mes queda cerrado (no admite más gastos) |
| Vencimiento | Día 10 del mes siguiente |
| Pagos | Pueden ser parciales; nunca mayores al saldo pendiente |
| Mora | 3 % del saldo por cada mes (o fracción) de atraso |
| Bajas | No se puede borrar un propietario con unidades ni una unidad con expensas emitidas |
| Ingreso de datos | 3 intentos por dato; si se agotan, se cancela la operación sin cerrar el programa |

## Temas de la materia aplicados

| Tema | Dónde |
|---|---|
| Matrices | Tabla anual de pagos (unidades × meses) en `reportes.construir_tabla_anual`; transpuesta en `utils.trasponer` para contar pagos por mes |
| Diccionarios, tuplas y conjuntos | Registros como diccionarios; catálogos en tuplas (`constantes.py`); `porcentaje_al_dia` con diferencia e intersección de conjuntos |
| Métodos de listas y cadenas, slicing | Paginación (`utils.paginar`), `piso_de_codigo` con `codigo[:-1]`, `formatear_moneda` con `replace`, `normalizar_nombre` con `split`/`join`/`title` |
| Listas por comprensión y lambda | `map`, `filter`, `reduce`, `sorted` y `next` en `reportes.py` y `services.py` |
| Expresiones regulares | Validaciones con `re.fullmatch` en `utils.py`; búsqueda de propietarios con `re.search` |
| Manejo de excepciones | `raise ValueError` en las reglas de negocio, `try/except` en `menus.ejecutar_menu`, `for…else` con máximo de intentos |
| Archivos | JSON por entidad, log en TXT (modo `"a"`) y exportación a CSV en `storage.py`; rutas con `pathlib` |
| Arquitectura en capas | Estructura `main.py` + `src/` |
| Pruebas unitarias y CI | `pytest`, `parametrize`, `unittest.mock.patch` y GitHub Actions |
