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