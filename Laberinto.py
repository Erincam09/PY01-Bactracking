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

prueba = crear_Matriz(25)
mostrar_matriz(prueba)