import tkinter as tk
from tkinter import ttk
import random

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto")
        self.root.geometry("800x600")

        self.crear_controles() 

    def crear_controles(self):
        """ 
         Aca vamos a poner el frame donde se situaran los botones de control
         y las configuraciones
        """
        frame_controles = ttk.Frame(self.root, padding="10")   #Frame controles
        frame_controles.pack(fill=tk.X)

        #Generar Laberinto btn
        btn_generar = ttk.Button(frame_controles, text="Generar Laberinto", command=self.generar_laberinto)  
        btn_generar.pack(side=tk.LEFT, padx=5)

        #Resolver Laberinto btn
        btn_resolver = ttk.Button(frame_controles, text="Mostrar caminos", command=self.resolver_laberinto)
        btn_resolver.pack(side=tk.LEFT, padx=5)

        #Seleccion de tamaño de laberinto, configuraciones
        label_tamaño = ttk.Label(frame_controles, text="Tamaño: ")
        label_tamaño.pack(side=tk.LEFT, padx=5)

        self.spin_tamano = ttk.Spinbox(frame_controles, from_=5, to=20, width=5) #un spinbox que vaya de 5x5 a 25x25 | Implementar
        self.spin_tamano.pack(side=tk.LEFT, padx=5)
        self.spin_tamano.set(10)

        self.frame_laberinto =ttk.Frame(self.root)
        self.frame_laberinto.pack(expand=True, fill=tk.BOTH)

    def generar_laberinto(self):
        print("Generando Bakcroom")

    def resolver_laberinto(self):
        print("Buscando ruta de escape")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()
"""
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
        if matriz[nodoInicio[0]][nodoInicio[1]] == 1:
            matriz[nodoInicio[0]][nodoInicio[1]] = 2
        else:
            return("El campo seleccionado no es valido")
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
tam = len(prueba)
final = nodo_final(prueba)
mostrar_matriz(prueba, None, final)
fil = int(input("Numero de fila:\n"))
if fil>=tam or fil<0:
    return("Error: fila invalida")
col = int(input("Numero de columna:\n"))
if col>=tam or col<0:
    return("Error: columna invalida")
mostrar_matriz(prueba, [fil,col], None)
print("\n")
caminos = backtracking(prueba, [fil,col])
if caminos != []:
    CaminoOptimo = mejorCamino(caminos)
    print("Todos los caminos posibles: ",caminos)
    print("Mejor Camino: ",CaminoOptimo)
else:
    print("El laberinto no tiene solucion")
"""