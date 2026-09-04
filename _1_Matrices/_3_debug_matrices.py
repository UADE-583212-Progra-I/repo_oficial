def gen_matriz_nula(n_filas , n_columnas):
    """
    Que hace genera una matriz nula de n x m dimensiones
    que recibe: argumentos: n_filas, n_columnas
    que retorna: una matriz nula
    """
    matriz = [] # declaro es una lista
    for i in range(n_filas): # se puede reemplazar i por _
        fila = [] # x 3
        for j in range(n_columnas): # se puede reemplazar j por _
            # fila.append(1 if i == j else 0)
            # fila.append(random.randint(0,9)) # random
            if i == j:
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila) # x 4
    return matriz # que retorna: una matriz nula

# Crear una matriz nula de 3 x 4
m_nula = gen_matriz_nula(3, 4)



