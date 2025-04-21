import tkinter as tk
from tkinter import ttk
import random
from collections import deque

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto")
        self.root.geometry("800x600")
        self.matriz = []
        self.caminos = []
        self.camino_actual = 0
        self.crear_laberinto_frame() 
        self.caminos_especiales = {}
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
        label_tamano = ttk.Label(frame_controles, text="Tamaño: ")
        label_tamano.pack(side=tk.LEFT, padx=5)

        self.spin_tamano = ttk.Spinbox(frame_controles, from_=5, to=20, width=5) #un spinbox que vaya de 5x5 a 25x25 | Implementar
        self.spin_tamano.pack(side=tk.LEFT, padx=5)
        self.spin_tamano.set(10)

        self.frame_laberinto =ttk.Frame(self.root)
        self.frame_laberinto.pack(expand=True, fill=tk.BOTH)

        #Boton camino siguiente
        self.btn_siguiente = ttk.Button(frame_controles, text= "Siguiente camino", command=self.mostrar_siguiente_camino,
                                        state=tk.DISABLED)
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)

        # Mensajes 
        self.mensaje_var = tk.StringVar()
        self.mensaje_var.set("Listo para generar laberinto")
        self.label_mensaje = ttk.Label(frame_controles, textvariable=self.mensaje_var,
                                       relief=tk.SUNKEN,padding=(5,2))
        self.label_mensaje.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.label_mensaje.config(
            font=('Arial', 10),
            anchor=tk.W,  # Alinear texto a la izquierda
            wraplength=300  # Permite múltiples líneas
        )

        frame_caminos = ttk.Frame(frame_controles)
        frame_caminos.pack(side=tk.LEFT, padx=10, pady=5)

        btn_corto = ttk.Button(frame_caminos, text="Camino corto", command=lambda: self.mostrar_camino_especial('corto'))
        btn_corto.pack(side=tk.LEFT, padx=2)

        btn_optimo = ttk.Button(frame_caminos, text="Camino óptimo", command=lambda: self.mostrar_camino_especial('optimo'))
        btn_optimo.pack(side=tk.LEFT, padx=2)

        btn_largo = ttk.Button(frame_caminos, text="Camino largo", command=lambda: self.mostrar_camino_especial('largo'))
        btn_largo.pack(side=tk.LEFT, padx=2)


    def crear_laberinto_frame(self):
        "Frame para dibujar el labertinto"
        self.frame_laberinto = ttk.Frame(self.root)
        self.frame_laberinto.pack(expand=True,fill=tk.BOTH, padx=10, pady=10)


    def generar_laberinto(self):
        try:
            tamano = int(self.spin_tamano.get())
            self.matriz = crear_Matriz(tamano)

            #Asegurar que las esquinas sean caminos
            self.matriz[0][0] = 1
            self.matriz[tamano-1][tamano-1] = 1

            #Limbiar y dibujar consola
            for widget in self.frame_laberinto.winfo_children():
                widget.destroy()

            self.dibujar_matriz()

            self.caminos = []
            self.camino_actual = 0
            self.btn_siguiente.config(state=tk.DISABLED)
            self.mostrar_mensaje("Laberinto  generado con exito", 'exito')
        except ValueError:
            self.mostrar_mensaje("Error: Por favor ingrese un tamaño de matriz válido (5x5 - 25x25)", 'error')


    def dibujar_matriz(self, camino=None):
        if camino is not None:
            color_camino = 'green'
            self.dibujar_matriz_especial(camino, color_camino)
        else:
            self.dibujar_matriz_especial([],None)

    

    def resolver_laberinto(self):
        "Encontrar todos los posibles caminos usando el algoritmo de Backtracking"
        if not self.matriz:
            self.mostrar_mensaje("Primero genera un laberinto", 'error')
            return
        
        self.matriz_original = [fila[:] for fila in self.matriz]


        #Seleccionar Posicion
        tamano = len(self.matriz)
        inicio = [0,0]
        fin = [tamano-1, tamano-1]

        #validar error en posicion con respecto a tamaño de matriz
        if self.matriz[inicio[0]][inicio[1]] != 1:
            self.mostrar_mensaje("Posición inicial no es válida", 'error')
            # Forzar posición inicial válida
            self.matriz[inicio[0]][inicio[1]] = 1
            self.matriz_original[inicio[0]][inicio[1]] = 1
        
        if self.matriz[fin[0]][fin[1]] != 1:
            self.mostrar_mensaje("Posición final no es válida", 'error')
            # Forzar posición final válida
            self.matriz[fin[0]][fin[1]] = 1
            self.matriz_original[fin[0]][fin[1]] = 1

        self.matriz[inicio[0]][inicio[1]] = 2 #Inicio
        self.matriz[fin[0]][fin[1]] = 3 #final
        self.dibujar_matriz()

        self.caminos = backtracking(self.matriz, inicio)

        if self.caminos:
            self.encontrar_caminos_especiales()
            self.mostrar_mensaje("Se encontraron " + str(len(self.caminos)) + " caminos", 'exito')
            self.camino_actual = 0
            self.dibujar_matriz(self.caminos[self.camino_actual])
            self.btn_siguiente.config(state=tk.NORMAL)

        else:
            self.mostrar_mensaje("No se encontraron caminos", 'error')
            self.matriz = [fila[:] for fila in self.matriz_original]
            self.dibujar_matriz()


#Encuentra los caminos mas corto, largo y optimo
    def encontrar_caminos_especiales(self):
        if not self.caminos:
            return
        self.caminos_especiales['corto'] = min(self.caminos, key=len)
        self.caminos_especiales['largo'] = max(self.caminos, key=len)
        self.caminos_especiales['optimo'] = self.encontrar_camino_optimo()


    def encontrar_camino_optimo(self):
        #Primero ordenamos por longitud
        caminos_ordenados = sorted(self.caminos, key=len)
        #Elegimos el 25% de los mas cortos
        mejores_caminos = caminos_ordenados[:max(1, len(caminos_ordenados)//4)]

        return min(mejores_caminos, key=self.calcular_cambios_direccion)
    

    def calcular_cambios_direccion(self,camino):
        cambios = 0
        if len(camino) < 2:
            return 0
        direccion_anterior = (
            camino[1][0] - camino[0][0],
            camino[1][1] - camino[0][1]
        )

        for i in range(2, len(camino)):
            direccion_actual = (
                camino[i][0] - camino[i-1][0],
                camino[i][1] - camino[i-1][1]
            )
            if direccion_actual != direccion_anterior:
                cambios += 1
                direccion_anterior = direccion_actual
        return cambios

    def mostrar_camino_especial(self,tipo):
        if not self.caminos or tipo not in self.caminos_especiales:
            return
        
        #resetear matriz
        self.matriz = [fila[:] for fila in self.matriz_original]

        tamano = len(self.matriz)
        self.matriz[0][0] = 2
        self.matriz[tamano-1][tamano-1] = 3

        color = {
            'corto': 'green',
            'optimo': 'yellow',
            'largo': 'orange'
        }.get(tipo, 'green')
        self.dibujar_matriz_especial(self.caminos_especiales[tipo], color)
        self.mostrar_mensaje("Mostrando camino "+ tipo, 'info')


    def dibujar_matriz_especial(self, camino, color_camino):
        """Dibuja la matriz resaltanmdp un camino con color especial"""
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                valor = self.matriz[i][j]

                if valor == 0:
                    bg_color = "gray20"
                    text = ""
                elif valor == 1:
                    bg_color = "white"
                    text = ""
                elif valor == 2:
                    bg_color = "blue"
                    text = "I"
                elif valor == 3:
                    bg_color = "red"
                    text = "F"
                if [i,j] in camino:
                    bg_color = color_camino
                    text = "•"
                celda = tk.Label(self.frame_laberinto, text=text, bg=bg_color, width=3,
                                 height=1, relief="ridge", font=('Arial',10))
                celda.grid(row=i, column=j, padx=1, pady=1)
    

    def mostrar_siguiente_camino(self):
        if not self.caminos:
            return
        
        self.matriz = [fila[:] for fila in self.matriz_original]

        #Volver a marcar inicio y fin
        tamano = len(self.matriz)
        self.matriz[0][0] = 2
        self.matriz[tamano-1][tamano-1] = 3

        #Siguiente Camino
        self.camino_actual = (self.camino_actual + 1) % len(self.caminos)
        self.dibujar_matriz_especial(self.caminos[self.camino_actual], 'green')


    def mostrar_mensaje(self, mensaje, tipo='info'):
        colores = {
            'info': 'black',
            'error': 'red',
            'exito': 'green',
            'debug': 'blue'
        }
        self.mensaje_var.set(mensaje)
        self.label_mensaje.config(foreground=colores.get(tipo, 'black'),
                                  font=('Arial', 10, 'italic' if tipo == 'debug' else 'normal'))
        self.root.update_idletasks()

#CAMBIO ------------------------------------------------------


def camino_valido(matriz):
    if not matriz or matriz[0][0] == 0 or matriz[-1][-1] == 0:
        return False

    tamano = len(matriz)
    visitados = [[False for _ in range(tamano)] for _ in range(tamano)]

    def dfs(x,y):
        if x == tamano-1 and y == tamano-1:
            return True
        
        visitados[x][y] = True
        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]

        for direccion in direcciones:
            dx, dy = direccion
            nuevo_x = x + dx
            nuevo_y = y + dy
            
            coordenada_valida = (0 <= nuevo_x < tamano and 0 <= nuevo_y < tamano)
            if coordenada_valida and not visitados[nuevo_x][nuevo_y] and matriz[nuevo_x][nuevo_y] == 1:
                if dfs(nuevo_x, nuevo_y):
                    return True
        return False
    return dfs(0,0) 


def crear_Matriz(tamano):
    """
    crear matriz dinamica, asegurando al menos un camino a punto b dejando las esquinas libres
    """
    intentos_maximos = 10
    for _ in range(intentos_maximos):
        matriz_temp = []
        for fila in range (tamano):
            fila_temp = []
            for columna in range(tamano):
                if (fila == 0 and columna == 0) or (fila == tamano-1 and columna == tamano-1):
                    fila_temp.append(1)
                else:
                    fila_temp.append(1 if random.random() < 0.7 else 0)
            matriz_temp.append(fila_temp)
        if camino_valido(matriz_temp):
            return matriz_temp
        
    #Generar laberrinto abierto despues de muchos intentos para que no explote
    return [[1 for _ in range(tamano)] for _ in range(tamano)]

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


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()
"""
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