import random

def crear_Matriz(tamano):
    matriz = []
    for fila in range(tamano):
        nueva_fila = []
        for columna in range(tamano):
            if random.random() < 0.7:
                nueva_fila.append(1)
            else:
                nueva_fila.append(0)
        matriz.append(nueva_fila)
    return matriz


def mostrar_matriz(matriz, nodoInicio, nodoFinal):
    if nodoInicio != None:
        matriz[nodoInicio[0]][nodoInicio[1]] = 2
    if nodoFinal != None:
        matriz[nodoFinal[0]][nodoFinal[1]] = 3
    for fila in matriz:
        print(fila)

def nodo_final(matriz):
    tam = len(matriz)
    posibles = []
    for i in range(tam):
        for j in range(tam):
            if matriz[i][j] == 1:
                posibles.append([i, j])
    if posibles != None:
        return random.choice(posibles)

def backtracking(matriz, nodoInicio):
    listaCaminos = []
    visitados = []
    busqueda(matriz, None, nodoInicio, [], listaCaminos, visitados)
    return listaCaminos

def busqueda(matriz, nodoAnterior, nodoActual, lista, listaCaminos, visitados):
    if(nodoActual[0] >= 0 and nodoActual[1] >= 0 and nodoActual[0] < len(matriz) and nodoActual[1] < len(matriz)):
        for elem in visitados:
            if elem == nodoActual:
                return
        if (matriz[nodoActual[0]][nodoActual[1]] == 3):
            listaCaminos += [lista + [nodoActual]]
        if (matriz[nodoActual[0]][nodoActual[1]] == 2 or matriz[nodoActual[0]][nodoActual[1]] == 1):
            visitados += [nodoActual]
            # Arriba
            if (nodoAnterior != [nodoActual[0]-1, nodoActual[1]]):
                busqueda(matriz, nodoActual, [nodoActual[0]-1, nodoActual[1]], lista + [nodoActual], listaCaminos, visitados)
            # Derecha
            if (nodoAnterior != [nodoActual[0], nodoActual[1]+1]):
                busqueda(matriz, nodoActual, [nodoActual[0], nodoActual[1]+1], lista + [nodoActual], listaCaminos, visitados)
            # Abajo
            if (nodoAnterior != [nodoActual[0]+1, nodoActual[1]]):
                busqueda(matriz, nodoActual, [nodoActual[0]+1, nodoActual[1]], lista + [nodoActual], listaCaminos, visitados)
            # Izquierda
            if (nodoAnterior != [nodoActual[0], nodoActual[1]-1]):
                busqueda(matriz, nodoActual, [nodoActual[0], nodoActual[1]-1], lista + [nodoActual], listaCaminos, visitados)

            visitados.pop()

def mejorCamino(lista):
    mejor = lista[0]
    for camino in lista:
        if len(camino)<len(mejor):
            mejor = camino
    return mejor

prueba = crear_Matriz(5)
final = nodo_final(prueba)
mostrar_matriz(prueba, None, final)
fil = int(input("Numero de fila:\n"))
col = int(input("Numero de columna:\n"))
mostrar_matriz(prueba, [fil,col], None)
print("\n")
caminos = backtracking(prueba, [fil,col])
CaminoOptimo = mejorCamino(caminos)
print(caminos)
print(CaminoOptimo)