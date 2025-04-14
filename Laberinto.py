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


def mostrar_matriz(matriz):
    for fila in matriz:
        print(" ".join("🟩" if num == 1 else "🚧" for num in fila))  # 1=🟩, 0=🚧

# prueba = crear_Matriz(25)
# mostrar_matriz(prueba)

def backtracking(matriz, nodoInicio, nodoFinal):
    matriz[nodoInicio[0]][nodoInicio[1]] = 2
    matriz[nodoFinal[0]][nodoFinal[1]] = 3
    listaCaminos = []
    busqueda(matriz, None, nodoInicio, [], listaCaminos)
    print(listaCaminos)

def busqueda(matriz, nodoAnterior, nodoActual, lista, listaCaminos):
    if(nodoActual[0] >= 0 and nodoActual[1] >= 0 and nodoActual[0] < len(matriz) and nodoActual[1] < len(matriz)):
        if (matriz[nodoActual[0]][nodoActual[1]] == 3):
            listaCaminos += [lista + [nodoActual]]
        if (matriz[nodoActual[0]][nodoActual[1]] == 2 or matriz[nodoActual[0]][nodoActual[1]] == 1):
            # Arriba
            if (nodoAnterior != [nodoActual[0]-1, nodoActual[1]]):
                busqueda(matriz, nodoActual, [nodoActual[0]-1, nodoActual[1]], lista + [nodoActual], listaCaminos)
            # Derecha
            if (nodoAnterior != [nodoActual[0], nodoActual[1]+1]):
                busqueda(matriz, nodoActual, [nodoActual[0], nodoActual[1]+1], lista + [nodoActual], listaCaminos)
            # Abajo
            if (nodoAnterior != [nodoActual[0]+1, nodoActual[1]]):
                busqueda(matriz, nodoActual, [nodoActual[0]+1, nodoActual[1]], lista + [nodoActual], listaCaminos)
            # Izquierda
            if (nodoAnterior != [nodoActual[0], nodoActual[1]-1]):
                busqueda(matriz, nodoActual, [nodoActual[0], nodoActual[1]-1], lista + [nodoActual], listaCaminos)
        

matriz = [[1,0,1,1,0],
          [1,1,0,1,0],
          [0,1,1,1,1],
          [0,0,1,0,1],
          [0,1,1,1,1]]

backtracking(matriz, [0,0], [3,4])