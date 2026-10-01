# 🎵 Actividad Integradora — Listas por Comprensión, Lambda y Arquitectura Modular
### Programación I | UADE

---

## Contexto

En la actividad anterior construimos el **Sistema de Recomendación Musical Parte 1**: un CRUD de usuarios, el registro de ratings y la construcción de la matriz de doble entrada.

En esta actividad vamos a hacer dos cosas en paralelo:

1. **Optimizar** las funciones existentes aplicando listas por comprensión y funciones lambda con `map`, `filter`, `sorted` y `reduce`.
2. **Reestructurar** el proyecto en una arquitectura modular separada en archivos, alineada con la estructura del TPO.

---

## Parte 1 — Optimización con listas por comprensión y lambda

Tomá el archivo `_4_actividad_integradora_template.py` como punto de partida y reescribí las funciones indicadas usando las herramientas vistas en clase.

> 💡 **Regla general:** si una función recorre una lista con `for` + `append` para transformar o filtrar, puede reemplazarse con una lista por comprensión o con `map`/`filter`. Si acumula un valor con `for` + suma, puede reemplazarse con `reduce`.

---

### 1.1 `buscar_tema_por_id` — reescribir con `next` + expresión generadora

La versión actual usa un `for` con `return` anticipado. Reescribila usando `next()` con una expresión generadora, que devuelve el primer elemento que cumple la condición o un valor por defecto:

```python
# Versión actual
for tema in TEMAS:
    if tema["id_tema"] == id_tema:
        return tema
return None

# Versión con next + generadora
return next((t for t in TEMAS if t["id_tema"] == id_tema), None)
```

Aplicá el mismo patrón a `buscar_usuario_por_id`.

---

### 1.2 `leer_usuarios` — reescribir con lista por comprensión

La función actual muestra los primeros usuarios con slicing y un `for`. Reescribí la parte de formateo usando una lista por comprensión que construya las líneas de texto:

```python
# Pista: podés construir una lista de strings formateados y luego imprimirlos
lineas = [f"  [{u['id_usuario']}] {u['nombre']} ..." for u in usuarios[:5]]
```

---

### 1.3 `construir_matriz_ratings` — reescribir con comprensión de dos niveles

La función actual construye la matriz con dos `for` anidados. Reescribila usando una comprensión de listas anidada:

```python
# Pista: la estructura es
matriz = [
    [indice.get((u["id_usuario"], t["id_tema"]), 0) for t in TEMAS]
    for u in usuarios_ord
]
```

El índice `(id_usuario, id_tema) → rating` también puede construirse con una comprensión de diccionario:

```python
indice = {(r["id_usuario"], r["id_tema"]): r["rating"] for r in ratings}
```

---

### 1.4 `registrar_rating` — agregar búsqueda con `next`

La función actual no verifica si el usuario ya calificó ese tema. Agregá esa lógica usando `next`:

```python
# Buscar si ya existe un rating para (id_usuario, id_tema)
existente = next(
    (r for r in ratings if r["id_usuario"] == id_usuario and r["id_tema"] == id_tema),
    None
)

# Si existe, actualizarlo. Si no, crear uno nuevo.
```

---

### 1.5 Nuevas funciones de estadísticas con `map`, `filter`, `reduce` y `sorted`

Agregá las siguientes funciones al sistema, implementándolas **exclusivamente** con las herramientas vistas:

**a) `promedio_ratings_tema(id_tema)`**
- Filtrá los ratings del tema con `filter` + `lambda`
- Extraé los valores con `map` + `lambda`
- Calculá la suma con `reduce` y dividí por la cantidad
- Retorná `0` si el tema no tiene ratings

**b) `ranking_temas()`**
- Calculá el promedio de cada tema usando `promedio_ratings_tema`
- Construí una lista de diccionarios `{"tema": ..., "promedio": ...}` con comprensión
- Ordená de mayor a menor con `sorted` + `lambda`
- Retorná la lista ordenada

**c) `temas_sin_calificar(id_usuario)`**
- Obtenés los `id_tema` ya calificados por el usuario con comprensión + `set`
- Filtrás los temas que **no** están en ese conjunto con comprensión
- Retorná la lista de diccionarios de temas pendientes

**d) `usuario_mas_activo()`**
- Para cada usuario, contá cuántos ratings tiene con `filter` + `len`
- Usá `max` con `lambda` como `key` para encontrar el más activo
- Retorná el diccionario del usuario

---

### Tabla de herramientas a aplicar

| Función | Herramienta |
|---|---|
| `buscar_tema_por_id` | `next` + expresión generadora |
| `buscar_usuario_por_id` | `next` + expresión generadora |
| `leer_usuarios` | Lista por comprensión |
| `construir_matriz_ratings` | Comprensión de diccionario + comprensión anidada |
| `registrar_rating` | `next` para detectar duplicado |
| `promedio_ratings_tema` | `filter`, `map`, `reduce` |
| `ranking_temas` | Comprensión + `sorted` + `lambda` |
| `temas_sin_calificar` | Comprensión + `set` |
| `usuario_mas_activo` | `filter` + `max` + `lambda` |

---

## Parte 2 — Arquitectura modular: estructura `src`

### ¿Por qué modularizar?

Un archivo único de 400+ líneas mezcla tres responsabilidades distintas:

- **Presentación**: lo que el usuario ve (menús, inputs, prints)
- **Lógica de negocio**: las reglas del sistema (validaciones, búsquedas, cálculos)
- **Datos**: las listas en memoria y las operaciones sobre ellas

Separar estas responsabilidades en archivos distintos hace el código más fácil de mantener, testear y reutilizar. Esta separación se llama **arquitectura en capas**.

---

### Estructura de archivos

Reorganizá el proyecto en la siguiente estructura:

```
sis-rec/
│
├── main.py                  ← punto de entrada, solo llama a interface
│
└── src/
    ├── data.py              ← datos iniciales (TEMAS, listas globales)
    ├── services.py          ← lógica de negocio (buscar, calcular, validar)
    ├── interface.py         ← menús, inputs y prints
    └── utils.py             ← utilidades reutilizables
```

---

### Descripción de cada archivo

#### `src/data.py` — datos globales
Contiene únicamente las listas y constantes que representan el estado del sistema. No tiene lógica ni prints.

```python
# src/data.py

TEMAS = [
    {"id_tema": 1, "tema": "Dai Dai",       "autor": "Shakira"},
    {"id_tema": 2, "tema": "Dynamite",       "autor": "BTS"},
    {"id_tema": 3, "tema": "DTMF",           "autor": "Bad Bunny"},
    {"id_tema": 4, "tema": "Dont Start Now", "autor": "Dua Lipa"},
    {"id_tema": 5, "tema": "Positions",      "autor": "Ariana Grande"},
]

usuarios = []
ratings  = []
```

---

#### `src/utils.py` — utilidades reutilizables
Funciones puras que no dependen del estado del sistema: validaciones de strings, generación de ids.

```python
# src/utils.py

def validar_nombre(nombre): ...
def validar_email(email): ...
def validar_id(valor): ...
def generar_id(lista, campo_id): ...
```

> Una función **pura** es la que siempre devuelve el mismo resultado para los mismos argumentos y no modifica nada externo. Las validaciones son el ejemplo perfecto.

---

#### `src/services.py` — lógica de negocio
Las operaciones sobre los datos: buscar, crear, eliminar, calcular estadísticas. Recibe las listas como parámetros (no las importa directamente de `data.py`).

```python
# src/services.py
from functools import reduce

def buscar_tema_por_id(temas, id_tema): ...
def buscar_usuario_por_id(usuarios, id_usuario): ...

def crear_usuario(usuarios, id_usuario, nombre, apellido, email): ...
def eliminar_usuario(usuarios, ratings, id_usuario): ...

def registrar_rating(ratings, id_usuario, id_tema, valor): ...

def promedio_ratings_tema(ratings, id_tema): ...
def ranking_temas(temas, ratings): ...
def temas_sin_calificar(temas, ratings, id_usuario): ...
def usuario_mas_activo(usuarios, ratings): ...

def construir_matriz_ratings(usuarios, temas, ratings): ...
```

> **Diferencia clave con la versión anterior:** las funciones de `services.py` reciben las listas como parámetros en lugar de acceder a variables globales. Esto las hace más fáciles de testear y reutilizar.

---

#### `src/interface.py` — presentación
Todo lo que interactúa con el usuario: `input()`, `print()` y los menús. Importa desde `services.py` y `data.py`, pero **nunca** contiene lógica de negocio.

```python
# src/interface.py
from src import data, services, utils

def menu_principal(): ...
def menu_usuarios(): ...
def menu_ratings(): ...

def flujo_crear_usuario(): ...      # pide datos, valida, llama a services
def flujo_registrar_rating(): ...   # pide datos, llama a services
def flujo_ver_ranking(): ...        # llama a services, formatea e imprime
```

---

#### `main.py` — punto de entrada
Un archivo mínimo que solo arranca la aplicación.

```python
# main.py
from src.interface import menu_principal

if __name__ == "__main__":
    menu_principal()
```

---

### Diagrama de dependencias

```
main.py
  └── interface.py
        ├── services.py
        │     └── utils.py (opcional)
        └── data.py
```

> **Regla:** las dependencias van de afuera hacia adentro. `interface.py` conoce a `services.py`, pero `services.py` **no conoce** a `interface.py`. Esto evita dependencias circulares.

---

### Consigna detallada

#### Paso 1 — Crear la estructura de carpetas

```bash
mkdir sis-rec
cd sis-rec
mkdir src
touch main.py src/__init__.py src/data.py src/utils.py src/services.py src/interface.py
```

El archivo `src/__init__.py` vacío le indica a Python que `src` es un paquete importable.

#### Paso 2 — Migrar `data.py`
Copiá `TEMAS`, `usuarios` y `ratings` desde el archivo original.

#### Paso 3 — Migrar `utils.py`
Copiá `validar_nombre`, `validar_email` y `validar_id_usuario`.  
Agregá `generar_id(lista, campo_id)` que retorne `max(lista, key=...) + 1` (o `1` si la lista está vacía).

#### Paso 4 — Migrar `services.py`
Reescribí todas las funciones de búsqueda, CRUD y estadísticas usando listas por comprensión y lambda (Parte 1 de esta actividad).  
Todas las funciones reciben las listas como parámetros.

#### Paso 5 — Migrar `interface.py`
Reescribí los menús y flujos de interacción. Cada "flujo" (crear usuario, registrar rating, ver ranking) debe:
1. Pedir los datos al usuario con `input()`
2. Validar con `utils`
3. Llamar a `services`
4. Mostrar el resultado con `print()`

#### Paso 6 — Escribir `main.py`
Importar y llamar a `menu_principal()`.

#### Paso 7 — Verificar
Ejecutar `python main.py` y probar que el sistema funciona igual que el archivo original.

---

## Criterios de evaluación

| Criterio | Descripción |
|---|---|
| Listas por comprensión | Todas las funciones indicadas usan comprensión en lugar de `for` + `append` |
| `map`, `filter`, `reduce` | Aplicados correctamente en las funciones de estadísticas |
| `next` + generadora | Usado en búsquedas por id |
| Separación de capas | Ninguna función de `services.py` tiene `input()` ni `print()` |
| Ninguna lógica en `interface.py` | Los flujos solo coordinan, no calculan |
| `data.py` sin lógica | Solo contiene listas y constantes |
| `main.py` mínimo | Una o dos líneas |
| Git | Al menos un commit por archivo creado |

---

## Entrega

- Repositorio GitHub con rama `develop` y merge final a `main`
- Estructura de carpetas respetando el layout `src/`
- Al menos 6 commits (uno por archivo)
- El sistema debe ejecutarse con `python main.py` sin errores

---

> 🚀 **Conexión con el TPO:** esta estructura modular es la base sobre la que en la Parte 2 del proyecto vamos a agregar la lógica de recomendación (`recomendador.py`) sin modificar ninguno de los archivos existentes — solo lo importamos desde `interface.py`.
