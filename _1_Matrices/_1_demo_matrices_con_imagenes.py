# Importar librerías
import matplotlib.pyplot as plt

# Declaracion de constantes

MATRIZ_NUMERICA = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

DIGITO_2_LR = [
    [0,   0,  40, 180, 220,  40,   0,  0],
    [0,  30, 200, 255, 255, 180,   0,  0],
    [0,   0,   0,  40, 220, 180,   0,  0],
    [0,   0,  30, 200, 255,  40,   0,  0],
    [0,   0, 180, 255, 180,   0,   0,  0],
    [0,  30, 220,  80,   0,   0,   0,  0],
    [0, 180, 255, 220, 180, 180,  30,  0],
    [0, 220, 255, 255, 255, 255, 180,  0],
]

DIGITO_2_HR = [
    [0,   0,   0,   0,  30,  80, 180, 220, 220, 180,  80,  30,   0,   0,   0,   0],
    [0,   0,   0,  30, 180, 220, 255, 255, 255, 255, 220, 180,  30,   0,   0,   0],
    [0,   0,  30, 180, 255, 255, 220, 180, 180, 220, 255, 255, 180,  30,   0,   0],
    [0,   0,  80, 220, 255, 180,  80,  40,  40,  80, 180, 255, 220,  80,   0,   0],
    [0,   0,  30, 180, 255, 180,   0,   0,   0,   0,  80, 220, 255, 180,  30,   0],
    [0,   0,   0,  30, 180,  80,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0],
    [0,   0,   0,   0,  30,   0,   0,   0,   0,   0,   0,  80, 255, 220,  80,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  30, 180, 255, 180,  30,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,   0,  30, 180, 255, 220,  80,   0,   0,   0,   0,   0,   0],
    [0,   0,   0,   0,  30, 180, 255, 220,  80,  80, 180, 220, 220, 180,  80,  30],
    [0,   0,   0,  30, 180, 255, 255, 255, 255, 255, 255, 255, 255, 255, 180,  30],
    [0,   0,  30, 180, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 180],
]

# Genera una matriz nula de m x n
def gen_matriz_nula(n_filas, n_columnas):
    matriz_nula = []
    for i in range(n_filas):
        fila = []
        for j in range(n_columnas):
            fila.append(0)
        matriz_nula.append(fila)
    return matriz_nula


# Transpone una matriz de m x n a otra de n x m
def trasponer(matriz):
    """
    Retorna la transpuesta de una matriz n x m.
    La transpuesta tiene dimensión m x n.
    """
    n_filas = len(matriz)
    n_columnas = len(matriz[0])

    # La transpuesta tiene dimensiones invertidas
    transpuesta = gen_matriz_nula(n_columnas, n_filas)

    for i in range(n_filas):
        for j in range(n_columnas):
            transpuesta[j][i] = matriz[i][j]

    return transpuesta


# Rota una matriz 90° en sentido horario
def rotar_90_horario(matriz):
    """
    Retorna la rotacion en sentido horario de una matriz de m x n.
    La rotada tiene dimensión n x m.
    """
    n_filas = len(matriz)
    n_columnas = len(matriz[0])

    # La transpuesta tiene dimensiones invertidas
    rotada = gen_matriz_nula(n_columnas, n_filas)

    for i in range(n_filas):  # 0,1,2
        for j in range(n_columnas):  # 0,1,2
            rotada[j][n_filas - 1 - i] = matriz[i][j]

    return rotada


# Rota una matriz 90° en sentido antihorario
def rotar_90_antihorario(matriz):
    """
    Retorna la rotacion de una matriz n x m.
    La rotada tiene dimensión m x n.
    """
    n_filas = len(matriz)
    n_columnas = len(matriz[0])

    # La transpuesta tiene dimensiones invertidas
    rotada = gen_matriz_nula(n_columnas, n_filas)

    for i in range(n_filas):  # 0,1,2
        for j in range(n_columnas):  # 0,1,2
            rotada[n_columnas - 1 - j][i] = matriz[i][j]

    return rotada


# Muestra una matriz en terminal
def mostrar_matriz(matriz):
    for fila in matriz:
        print(fila)


# Muestra un plot en un pop-up
def plot_digito(matriz):
    plt.imshow(matriz, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    plt.show()


# Gestión del submenú 1
def submenu1(matriz):
    while True:
        print("""
    SUBMENU 1
    1. Trasponer
    2. Rotar 90° horario
    3. Rotar 90° antihorario
    4. Volver
    """)
        subopcion = input("Ingrese subopción: ")
        match subopcion:
            case "1":
                matriz = trasponer(matriz)
                mostrar_matriz(matriz)
            case "2":
                matriz = rotar_90_horario(matriz)
                mostrar_matriz(matriz)
            case "3":
                matriz = rotar_90_antihorario(matriz)
                mostrar_matriz(matriz)
            case "4":
                break
            case _:
                print("Opción inválida")


# Gestión del submenú 2
def submenu2(matriz):
    while True:
        print("""
    SUBMENU 2
    1. Rotar 90° horario
    2. Rotar 90° antihorario
    3. Volver
    """)
        subopcion = input("Ingrese subopción: ")
        match subopcion:
            case "1":
                matriz = rotar_90_horario(matriz)
                plot_digito(matriz)
            case "2":
                matriz = rotar_90_antihorario(matriz)
                plot_digito(matriz)
            case "3":
                break
            case _:
                print("Opción inválida")

# Función principal
def main():
    # Seleccionar matriz
    while True:
        print("""
        MENU
        1. Matriz numérica
        2. Matriz dígito 2 - low resolution
        3. Matriz dígito 2 - high resolution
        4. Salir
        """)
        opcion = input("Ingrese su opción: ")
        match opcion:
            case "1":
                matriz = MATRIZ_NUMERICA
                mostrar_matriz(matriz)
                submenu1(matriz)

            case "2":
                matriz = DIGITO_2_LR
                plot_digito(matriz)
                submenu2(matriz)

            case "3":
                matriz = DIGITO_2_HR
                plot_digito(matriz)
                submenu2(matriz)

            case "4":
                break

            case _:
                print("Opción inválida")


if __name__ == "__main__":
    main()



