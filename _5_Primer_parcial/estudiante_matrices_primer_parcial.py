DIGITO_9 = [
    [0,   180, 180,   0],
    [180,   0,   0, 180],
    [180,   0,   0, 180],
    [0,   180, 180, 180],
    [0,     0,   0, 180],
    [0,     0,   0, 180],
    [0,     0,   0, 180],
    [0,   180, 180,   0],
]


def gen_matriz_nula(n_filas, n_columnas):
    matriz_nula = []
    # Completar
    return matriz_nula

def gen_negativo(matriz):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    matriz_negativo = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            # Completar
    return matriz_negativo


def gen_mirror_horizontal(matriz):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    mirror_horizontal = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            mirror_horizontal[i][j] = matriz[n_filas-1-i][j]
    return mirror_horizontal

def mostrar_matriz(matriz):
    for fila in matriz:
        print(fila)

def procesar_digito_9():
    matriz = DIGITO_9
    print(f"\nMatriz original")
    mostrar_matriz(matriz)

    matriz_negativo = gen_negativo(matriz)
    print(f"\nMatriz negativo")
    mostrar_matriz(matriz_negativo)

    matriz_mirror_horizontal = gen_mirror_horizontal(matriz)
    print(f"\nMatriz mirror horizontal")
    mostrar_matriz(matriz_mirror_horizontal)
