import tkinter as tk
from tkinter import ttk
import random

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto")
        self.root.geometry("800x600")
        self.matriz = []
        self.caminos = []
        self.camino_actual = 0
        self.crear_controles()
        self.crear_laberinto_frame() 

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


    def crear_laberinto_frame(self):
        "Frame para dibujar el labertinto"
        self.frame_laberinto = ttk.Frame(self.root)
        self.frame_laberinto.pack(expand=True,fill=tk.BOTH, padx=10, pady=10)


    def generar_laberinto(self):
        try:
            tamano = int(self.spin_tamano.get())
            self.matriz = crear_Matriz(tamano)
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
        "Dibuja la matriuz en el frame_laberinto"
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                valor = self.matriz[i][j]
                if valor == 0:
                    bg_color = "gray20"
                    text = ""
                elif valor == 1:
                    bg_color = "white"
                    text=""
                elif valor == 2: 
                    bg_color = "blue"
                    text="I"
                elif valor == 3:
                    bg_color = "red"
                    text="F"
                if camino and [i,j] in camino:
                    bg_color = "green"
                    text="•"

                celda = tk.Label(self.frame_laberinto, text=text, bg=bg_color,
                                 width=3, height=1, relief="ridge",font=('Arial', 10))
                celda.grid(row=i, column=j, padx=1, pady=1)

    

    def resolver_laberinto(self):
        "Encontrar todos los posibles caminos usando el algoritmo de Backtracking"
        if not self.matriz:
            self.mostrar_mensaje("Primero genera un laberinto", 'error')
            return
        
        


        #Seleccionar Posicion
        tamano = len(self.matriz)
        inicio = [0,0]
        fin = [tamano-1, tamano-1]

        #validar error en posicion con respecto a tamaño de matriz
        if self.matriz[inicio[0]][inicio[1]] != 1:
            self.mostrar_mensaje("Posición inicial no es válida", 'error')
            return
        
        if self.matriz[fin[0]][fin[1]] != 1:
            self.mostrar_mensaje("Posición final no es válida | Genere el laberinto nuevamente", 'error')
            return

        self.matriz[inicio[0]][inicio[1]] = 2 #Inicio
        self.matriz[fin[0]][fin[1]] = 3 #final
        self.dibujar_matriz()

        self.caminos = backtracking(self.matriz, inicio)

        if self.caminos:
            self.mostrar_mensaje("Se encontraron " + str(len(self.caminos)) + " caminos", 'exito')
            self.camino_actual = 0
            self.dibujar_matriz(self.caminos[self.camino_actual])
            self.btn_siguiente.config(state=tk.NORMAL)

        else:
            self.mostrar_mensaje("No se encontraron caminos", 'error')
            self.dibujar_matriz()

    
    def mostrar_siguiente_camino(self):
        if self.caminos:
            self.camino_actual = (self.camino_actual + 1) % len(self.caminos)
            self.dibujar_matriz(self.caminos[self.camino_actual])


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

"""
crear matriz dinamica, asegurando al menos un camino a punto b dejando las esquinas libres
"""
def crear_Matriz(tamano):
    matriz = []
    for fila in range(tamano):
        nueva_fila = []
        for columna in range(tamano):
            if (fila == 0 and columna == 0) or (fila == tamano-1 and columna == tamano-1):
                nueva_fila.append(1)
            else:  
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