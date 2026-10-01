# Importar librerías
import matplotlib.pyplot as plt

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
    for _ in range(n_filas):
        fila = []
        for _ in range(n_columnas):
            fila.append(0)
        matriz_nula.append(fila)
    return matriz_nula

def gen_nula_lxc(n_filas, n_columnas):
    matriz_nula = [0*n_columnas for _ in range(n_filas)]


def gen_negativo(matriz):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    matriz_negativo = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            matriz_negativo[i][j] = 255-matriz[i][j]
    return matriz_negativo

def gen_binaria(matriz, umbral):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    matriz_binaria = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            matriz_binaria[i][j] = 0 if matriz[i][j] < umbral else 255
    return matriz_binaria

def gen_mirror_horizontal(matriz):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    mirror_horizontal = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            mirror_horizontal[i][j] = matriz[i][n_columnas-1-j]
    return mirror_horizontal

def gen_mirror_vertical(matriz):
    n_filas = len(matriz)
    n_columnas = len(matriz[0])
    mirror_vertical = gen_matriz_nula(n_filas, n_columnas)
    for i in range(n_filas):
        for j in range(n_columnas):
            mirror_vertical[i][j] = matriz[n_filas-1-i][j]
    return mirror_vertical

def mostrar_matriz(matriz):
    for fila in matriz:
        print(fila)

def main():
    matriz = DIGITO_9
    print(f"\nMatriz original")
    mostrar_matriz(matriz)
    matriz_negativo = gen_negativo(matriz)
    print(f"\nMatriz negativo")
    mostrar_matriz(matriz_negativo)
    matriz_binario = gen_binaria(matriz, 128)
    print(f"\nMatriz binario")
    mostrar_matriz(matriz_binario)
    matriz_mirror_horizontal = gen_mirror_horizontal(matriz)
    print(f"\nMatriz mirror horizontal")
    mostrar_matriz(matriz_mirror_horizontal)

if __name__ == "__main__":
    main()