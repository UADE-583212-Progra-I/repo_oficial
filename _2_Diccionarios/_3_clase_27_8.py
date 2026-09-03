numero = 1
print(f"id_numero: {id(numero)} - numero {numero}")
numero = 2
print(f"id_numero: {id(numero)} - numero {numero}")
numero = 1
print(f"id_numero: {id(numero)} - numero {numero}")

lista = [1]
print(f"{id(lista)} - {lista}")
lista.append(2)
print(f"{id(lista)} - {lista}")
# Estructura: Lista de listas

# Creamos una lista para cada registro
artista_1 = [1, "Bansky", "Inglaterra"]
artista_2 = [2, "Kusama", "Japon"]

# Creamos la lista (Matriz):
artistas = [artista_1, artista_2]

print("Vista preliminar:")
# print(artistas[0][2])
for a in artistas:
    print(a[2])

"""
# De manera dinámica con append
artista = [3, "Koons", "EEUU"]

artistas.append(artista)

print("\nVista preliminar:")
for a in artistas:
    print(a)

"""

lista = [1,2,3]
lista1 = lista
print(id(lista), id(lista1))
lista1 = lista.copy()
print(id(lista), id(lista1))
print(type(lista))
print(type(numero))


# -----
# variable global 
lista = [1]

def sumar (lista):
    print(f"numero id en funcion sumar{id(lista)}")
    lista[0] = lista[0]+2
    return 

print(f"numero id global{id(lista.copy())}")
sumar(lista)
print(f"numero id global return sumar{id(lista)} - {lista}")