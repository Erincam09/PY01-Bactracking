import tkinter as tk
from tkinter import ttk
import random
from collections import deque
import json
from PIL import Image, ImageTk
from tkinter import messagebox
import os

Guardado = False
class InterfazLaberinto:
    def __init__(self):
        global Guardado
        self.menu_window = tk.Tk()
        ancho_pantalla = self.menu_window.winfo_screenwidth()
        alto_pantalla = self.menu_window.winfo_screenheight()
        alto_ventana = 600
        ancho_ventana = 1000
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.menu_window.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.menu_window.resizable(0, 0)
        self.menu_window.overrideredirect(True)
        self.fondo_menu()
        self.botones_menu()
        Guardado = False
        self.menu_window.mainloop()
        

    """
    Funcion para cargar automaticamente el fondo elegido para el menu al iniciar la app
    """
    def fondo_menu(self):
        try:
            self.bg_image = Image.open("pic/fondo_menu.png")
            self.bg_image = self.bg_image.resize((1000, 600), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                
            # Crea un Label con la imagen
            bg_label = tk.Label(self.menu_window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print("Error al cargar imagen", e)
            self.menu_window.config(bg="black")

    """
    Carga los botones del menu inicial despues de cargar la imagen
    """
    def botones_menu(self):
        # espacio para el titulo 
        title_frame = tk.Frame(self.menu_window, bg='')
        title_frame.pack(pady=(100, 20))  

        #Frame Contenedor de botones para el menu principal
        button_frame = tk.Frame(self.menu_window, bg='#1e1e1e')  # Frame transparente
        button_frame.pack(pady=(22, 30))

        #Estilo para los botones
        button_style = {
            "font": ("Comic Sans MS", 15, "bold"),
            "bd": 4,
            "relief": "raised",
            "fg": "#fce5cd",
            "bg": "#5c3b22",
            "activebackground": "#70492a",
            "activeforeground": "#fff5e1",
            "padx": 30,
            "pady": 2
        } 
        #Boton 1 (Modo Clasico)
        tk.Button(
            button_frame,
            text="Modo Clásico",
            command=self.iniciar_juego_clasico,
            **button_style
        ).pack(side=tk.LEFT, padx=15)

        #Boton 2 (Modo jugador)
        tk.Button(
            button_frame,
            text="Libre",
            command=self.iniciar_juego_libre,
            **{**button_style, "bg": "#7f8c8d", "activebackground": "#6c7a89"}
        ).pack(side=tk.LEFT, padx=15)

        # Botón Cargar Juego
        tk.Button(
            button_frame,
            text="Cargar Juego",
            command=self.cargar_juego,
            **button_style
        ).pack(side=tk.LEFT, padx=15)

        # Boton Salir
        tk.Button(
            button_frame,
            text="Salir",
            command=self.menu_window.destroy,  # Cierra la aplicación
            **{**button_style, 
            "bg": "#7b241c",  # Rojo oscuro/marrón
            "activebackground": "#922b21",
            "fg": "#fadbd8"}  # Texto más claro
        ).pack(side=tk.LEFT, padx=15)
        
    def iniciar_juego_clasico(self):
        self.menu_window.destroy()
        JuegoClasico(None)

    def iniciar_juego_libre(self):
        self.menu_window.destroy()
        JuegoLibre(None)

    def cargar_juego(self):
        Partidas = []
        self.Modo = None
        if not os.path.exists("Partidas.json") or os.path.getsize("Partidas.json") == 0:
            messagebox.showinfo("Intentelo despues", "No hay ninguna partida guardada")
            return
        else:
            with open("Partidas.json", "r") as archivo:
                Partidas = json.load(archivo)
                nombres = [partida["Numero de la Partida"] for partida in Partidas.values()]  # Cambié esta línea

        # Crear la ventana para cargar partida
        self.CargarJ = tk.Tk()
        self.CargarJ.title("Laberinto - Cargar Partida")
        ancho_pantalla = self.CargarJ.winfo_screenwidth()
        alto_pantalla = self.CargarJ.winfo_screenheight()
        alto_ventana = 350
        ancho_ventana = 500
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.CargarJ.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.CargarJ.config(bg='#2d3436')
        self.CargarJ.resizable(0, 0)
        self.CargarJ.overrideredirect(True)
        label2 = tk.Label(self.CargarJ, text="Seleccione el numero de partida:", font=("Courier new", 15, "bold"), fg="white", bg="#2d3436").place(x=56, y= 30)
        self.combo_partidas = ttk.Combobox(self.CargarJ, values=nombres, state="readonly", foreground="black", width=60, height = 100)
        self.combo_partidas.place(x=50, y=80)

        self.boton_volver = tk.Button(self.CargarJ, text="Volver", font=("Courier new", 15, "bold"), fg="#5c3b22", command=self.CargarJ.destroy)
        self.boton_volver.place(x=390, y=300)
        self.label1 = tk.Label(self.CargarJ, text="Elige un modo de juego:", font=("Courier new", 15, "bold"), fg="white", bg="#2d3436").place(x=110, y= 118)
        self.boton_clasico = tk.Button(self.CargarJ, text="Modo Clasico", font=("Courier new", 15, "bold"), fg="#7f8c8d", bg="white", width=15, command=lambda:self.M_Clasico(self.boton_clasico, self.boton_libre))
        self.boton_clasico.place(x=50, y=165)
        self.boton_libre = tk.Button(self.CargarJ, text="Modo Libre", font=("Courier new", 15, "bold"), fg="#7f8c8d", bg="white",width=15, command=lambda:self.M_Libre(self.boton_clasico, self.boton_libre))
        self.boton_libre.place(x=245, y=165)
        self.boton_cargar = tk.Button(self.CargarJ, text="Cargar Partida", font=("Courier new", 15, "bold"), fg="#5c3b22", bg="white",width=15, command=lambda:self.CargarJuego())
        self.boton_cargar.place(x=150, y=240)

        self.CargarJ.mainloop()
    
    def M_Clasico(self, clasico, libre):
        libre.config(fg="#7f8c8d")
        clasico.config(fg="#5c3b22")
        self.Modo =True

    def M_Libre(self, clasico, libre):
        clasico.config(fg="#7f8c8d")
        libre.config(fg="#5c3b22")
        self.Modo = False

    def CargarJuego(self):
        partida = self.combo_partidas.get()
        self.CargarJ.destroy()

        with open("Partidas.json", "r") as archivo:
            Partidas = json.load(archivo)

        partida_encontrada = None
        for juego in Partidas.values():
            if juego["Numero de la Partida"] == partida:
                partida_encontrada = juego
                break

        if partida_encontrada:
            matriz = partida_encontrada["Matriz"]

        if self.Modo == True:
            JuegoClasico(matriz)
        if self.Modo == False:
            JuegoLibre(matriz)
        if self.Modo == None:
            messagebox.showinfo("Error", "Debe de escoger un modo de juego")
            return
    
class JuegoBase:
    def __init__(self, matriz):
        global Guardado
        self.juego = tk.Tk()
        self.juego.title("Laberinto")
        self.juego.attributes('-fullscreen', True)
        if matriz == None:
            self.matriz = None
        else:
            self.matriz = matriz
            Guardado = True
        self.caminos = []
        self.camino_actual = 0
        self.caminos_especiales = {}
        self.mensaje_var = tk.StringVar()
        self.btn_siguiente = None 
        self.label_mensaje = None 
        self.juego.config(bg='#2d3436')
        self.setup_controles()
        self.setup_estilos()

    def setup_controles(self):
        global Guardado
         # Frame principal
        self.frame_principal = tk.Frame(self.juego, bg='#2d3436')
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.frame_controles = tk.Frame(self.frame_principal, bg='#3c3f41', padx=10, pady=10)
        self.frame_controles.grid(row=0, column=0, sticky="ew")

        #Area del laberinto 
        self.frame_laberinto = tk.Frame(self.frame_principal, bg='#2d3436', width = 900, height = 700)
        self.frame_laberinto.grid(row=1, column=0)

        #Botones Comunes
        ttk.Button(self.frame_controles, text="Generar Laberinto", command=self.generar_laberinto).pack(side=tk.LEFT, padx=5)
        
        # Selector de tamaño
        if Guardado == False:
            self.combo_dimensiones = ttk.Combobox(self.frame_controles, values=[5,10,15,20,25], state="readonly", foreground = "black")
            self.combo_dimensiones.pack(side=tk.LEFT, padx=5)
            self.combo_dimensiones.set(10)

        self.label_mensaje = ttk.Label(
            self.frame_controles,
            textvariable=self.mensaje_var,
            relief=tk.SUNKEN,
            padding=(5,2),
            background='white',
        )
        self.label_mensaje.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        ttk.Button(self.frame_principal, text="Volver al Menú", command=self.volver_menu).place(x=1230,y=720)

    def setup_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6, background='#3c3f41', foreground='white')
        style.map('TButton', background=[('active', '#0984e3')])
        style.configure('TCombobox', fieldbackground='#3c3f41', foreground='white')

    """
    Genera un laberinto válido mediante el siguiente proceso:
    1. Obtiene el tamaño seleccionado por el usuario
    2. Crea una matriz aleatoria usando crear_Matriz()
    3. Fuerza las esquinas (0,0) y (n-1,n-1) como celdas transitables
    4. Limpia el frame de dibujo anterior
    5. Reinicia el estado de caminos encontrados
    6. Maneja errores de entrada con mensajes visuales
    """
    def generar_laberinto(self):
        global Guardado
        try:
            if not Guardado:
                tamano = int(self.combo_dimensiones.get())
                self.matriz = crear_Matriz(tamano)

                # Marcadores de inicio y fin nuevos
                self.jugador_pos = [1, 1]
                self.matriz[1][1] = 2

                self.fin_pos = nodo_Aleatorio(self.matriz)
                self.matriz[self.fin_pos[0]][self.fin_pos[1]] = 3

            else:
                inicio = None
                final = None
                for i in range(len(self.matriz)):
                    for j in range(len(self.matriz[0])):
                        if self.matriz[i][j] == 2:
                            inicio = [i, j]
                        elif self.matriz[i][j] == 3:
                            final = [i, j]
                        elif self.matriz[i][j] == 5:
                            self.matriz[i][j] = 2
                            inicio = [i, j]

                for i, fila in enumerate(self.matriz):
                    for j, celda in enumerate(fila):
                        if celda == 2 and [i, j] != inicio:
                            self.matriz[i][j] = 1
                        if celda == 3 and [i, j] != final:
                            self.matriz[i][j] = 1
                        if celda == 4:
                            self.matriz[i][j] = 1

                self.jugador_pos = inicio
                self.fin_pos = final

                Guardado = False

            for widget in self.frame_laberinto.winfo_children():
                widget.destroy()
            self.botones = []
            for i in range(len(self.matriz)):
                fila = []
                for j in range(len(self.matriz[0])):
                    btn = tk.Button(
                        self.frame_laberinto, width=3, height=1,
                        relief="raised", font=('Arial', 10),
                        command=lambda x=i, y=j: self.NodoInicio(x, y)
                    )
                    btn.grid(row=i, column=j, padx=1, pady=1)
                    fila.append(btn)
                self.botones.append(fila)

            self.dibujar_matriz()

            self.caminos = []
            self.camino_actual = 0
            if hasattr(self, 'btn_siguiente'):
                self.btn_siguiente.config(state=tk.DISABLED)

            self.mostrar_mensaje("Laberinto generado con éxito", 'exito')

        except ValueError:
            self.mostrar_mensaje("Error: Por favor ingrese un tamaño de matriz válido (5x5 - 25x25)", 'error')
        except IndexError as e:
            self.mostrar_mensaje(f"Error al generar laberinto: {e}", 'error')


    def dibujar_matriz(self, camino=None):
        if camino is not None:
            color_camino = 'green'
            self.dibujar_matriz_especial(camino, color_camino)
        else:
            self.dibujar_matriz_especial([],None)

    """
    Sistema de renderizado gráfico del laberinto:
    - Asigna colores específicos a:
      * 0 (muro): gris oscuro
      * 1 (camino): blanco
      * 2 (inicio): azul
      * 3 (fin): rojo
    - Resalta celdas del camino con el color especificado
    """

    def dibujar_matriz_especial(self, camino, color_camino):
        """Dibuja la matriz resaltanmdp un camino con color especial"""
        if not hasattr(self, 'botones'):
            self.botones = []
            for i in range(len(self.matriz)):
                fila_botones = []
                for j in range(len(self.matriz[i])):
                    boton = tk.Button(
                        self.frame_laberinto, width=3, height=1,
                        relief="raised", font=('Arial', 10),
                        command=lambda x=i, y=j: self.NodoInicio(x, y)
                    )
                    boton.grid(row=i, column=j, padx=1, pady=1)
                    fila_botones.append(boton)
                self.botones.append(fila_botones)

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                valor = self.matriz[i][j]
                g_color = "#636e72" if valor == 0 else "#dfe6e9"  # Muro/Camino base
                boton = self.botones[i][j]
                text = ""
                estado = tk.NORMAL
                if valor == 0:
                    bg_color = "gray20"
                    text = ""
                    estado = tk.DISABLED
                elif valor == 1:
                    bg_color = "white"
                    text = ""
                    estado = tk.NORMAL
                elif valor == 2:
                    bg_color = "#3498db"
                    text = "J"
                    estado = tk.NORMAL
                elif valor == 3:
                    bg_color = "#e74c3c"
                    text = "F"
                    estado = tk.NORMAL
                elif valor == 4:
                    bg_color = "DeepSkyBlue3"
                    text = "•"
                    estado = tk.NORMAL
                elif valor == 5:
                    bg_color = "sea green"
                    text = "I"
                    estado = tk.NORMAL
                elif [i,j] == self.jugador_pos:
                    bg_color = "#3498db"
                    text = "J"
                if [i, j] in camino:
                    bg_color = color_camino
                    text = "•"

                boton.config(
                text=text,
                bg=bg_color,
                state=estado
                )

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
        self.juego.update_idletasks()

    def volver_menu(self):
        self.juego.destroy()
        InterfazLaberinto()

    """
    Funcion para guardar las partidas 
    -Crea una nueva ventana, en esta se solicita el numero de partida y empieza el proceso de guardado
    -Esta funcion verifica que exista un archivo json
    -En caso de que no exita el archivo, la funcion se encargara de crearlo
    """
    def guardar(self):
        self.partida_window = tk.Tk()
        self.partida_window.geometry("400x200")
        self.partida_window.title("Partida")
        self.partida_window.resizable(0, 0)
        self.partida_window.config(bg="#7f8c8d")
        self.label_nombre = tk.Label(self.partida_window,text="Ingrese el número de la partida:", bg="#7f8c8d", font = ("Comic Sans MS", 16),
        activeforeground="#fff5e1", fg="black")
        self.label_nombre.place(x=35, y=30)
        self.nombrePart = tk.Entry(self.partida_window, relief="sunken", font=("Courier New", 12), width=32)
        self.nombrePart.place(x=35, y=80)
        self.boton = tk.Button(self.partida_window,text="Guardar Partida", font=("Comic Sans MS", 12), bg="white", fg="black", command=lambda:self.agregarPartida(self.nombrePart.get(), self.partida_window))
        self.boton.place(x=111, y=130)

        nombreArchivo = "Partidas.json"
        try:
            archivo = open("Partidas.json","r")
            archivo.close()
        except:
            archivo = open(nombreArchivo,"w")
            archivo.write("{}")
            archivo.close()

        self.partida_window.mainloop()

    """
    Esta funcion recopila la informacion de la partida 
    Abre el archivo json y agrega la partida 
    Se guarda la matriz correspondiente con la partida y el numero ingresado anteriormente.
    Se muestra un mensaje de que la partida ha sido guardada satisfactoriamente.
    """
    def agregarPartida(self, nombre, ventana):
        if nombre == "" or not nombre.isdigit():
            messagebox.showerror("Error","Debe de ingresar un numero")
            ventana.destroy()
            return 

        Partidas = {}
        
        try:
            with open("Partidas.json", "r") as archivo:
                Partidas = json.load(archivo)
        except:
            Partidas = {}

        # Ahora sí agregamos la nueva partida
        nueva_partida = {
            "Numero de la Partida": nombre,
            "Matriz": self.matriz
        }
        
        if nombre in Partidas:
            messagebox.showerror("Error", "¡Este número de partida ya existe! Elija otro.")
            return

        Partidas[nombre] = nueva_partida  

        with open("Partidas.json", "w") as archivo:
            json.dump(Partidas, archivo, indent=7)

        ventana.destroy()
        messagebox.showinfo("Guardado", "Tu partida ha quedado guardada")


#--------------------------------------------------------------------------------   
""""
    Construye el panel de control superior con todos los elementos interactivos:
    - Botones para generación y resolución del laberinto
    - Selector de tamaño mediante Spinbox (rango 5-20)
    - Botones de navegación entre caminos
    - Sección especial para mostrar caminos destacados
    - Área de mensajes con sistema de colores por tipo (error/éxito/info)
    - Configura estilos y disposición de todos los widgets
"""
class JuegoClasico(JuegoBase):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setup_controles_clasico()
        # Inicialización de variables específicas
        self.caminos = []
        self.camino_actual = 0
        self.caminos_especiales = {}

    def setup_controles_clasico(self):
        global Guardado
        # Botones específicos del modo clásico
        self.frame_navegacion = tk.Frame(self.frame_controles, bg='#3c3f41')
        self.frame_navegacion.pack(side=tk.LEFT, padx=10)
        
         # Botón Resolver
        ttk.Button(
            self.frame_navegacion,
            text="Resolver Laberinto",
            command=self.resolver_laberinto,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón Siguiente Camino
        self.btn_siguiente = ttk.Button(
            self.frame_navegacion,
            text="Siguiente Camino",
            command=self.mostrar_siguiente_camino,
            state=tk.DISABLED,
            style='TButton'
        )
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)

        if Guardado == False:
            self.botonGuardar = self.botonGuardar = ttk.Button(
                self.frame_controles, 
                text="Guardar Partida", 
                command=self.guardar, 
                state = tk.DISABLED,
                style = 'TButton')
            self.botonGuardar.pack(side=tk.RIGHT, padx=5)

         # Botones de caminos especiales
        frame_especiales = ttk.Frame(self.frame_controles)
        frame_especiales.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame_especiales, text="Caminos:").pack(side=tk.LEFT)
        
         # Botones de caminos especiales
        ttk.Button(
            frame_especiales,
            text="Más Corto",
            command=lambda: self.mostrar_camino_especial('corto'),
            style='TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            frame_especiales,
            text="Óptimo",
            command=lambda: self.mostrar_camino_especial('optimo'),
            style='TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            frame_especiales,
            text="Más Largo",
            command=lambda: self.mostrar_camino_especial('largo'),
            style='TButton'
        ).pack(side=tk.LEFT, padx=2)
        
        # Configuración de estilos específicos
        self.style = ttk.Style()
        self.style.configure('Special.TButton', 
                                foreground='white',
                                background='#3498db',
                                font=('Arial', 10, 'bold'))
    
    """
    Coordina el proceso de resolución completo:
    1. Valida que exista un laberinto generado
    2. Crea copia de seguridad de la matriz original
    3. Configura puntos inicial (2) y final (3)
    4. Ejecuta el algoritmo de backtracking para encontrar todos los caminos
    5. Identifica caminos especiales (corto/largo/óptimo)
    6. Habilita la navegación entre soluciones
    7. Proporciona feedback visual del resultado
    """
    def resolver_laberinto(self):
        global Guardado
        "Encontrar todos los posibles caminos usando el algoritmo de Backtracking"
        if not self.matriz:
            self.mostrar_mensaje("Primero genera un laberinto", 'error')
            return

        # Verificar que haya inicio (forma correcta)
        inicio_encontrado = any(2 in fila for fila in self.matriz)
    
        if not inicio_encontrado:
            self.mostrar_mensaje("Debes seleccionar un punto de inicio primero", 'error')
            return

        self.matriz_original = [fila[:] for fila in self.matriz]
        self.caminos, self.Pasos = backtracking(self.matriz)

        if self.caminos:
            self.encontrar_caminos_especiales()
            self.mostrar_mensaje("Se encontraron " + str(len(self.caminos)) + " caminos", 'exito')
            self.camino_actual = 0
            self.dibujar_matriz(self.caminos[self.camino_actual])
            if hasattr(self, 'btn_siguiente'):
                self.btn_siguiente.config(state=tk.NORMAL)
                if Guardado == False:
                    self.botonGuardar.config(state=tk.NORMAL)
            else:
                self.mostrar_mensaje("No se encontraron caminos", 'error')
                self.matriz = [fila[:] for fila in self.matriz_original]
                self.dibujar_matriz()

    def mostrar_siguiente_camino(self):
        if not hasattr(self, 'caminos') or not self.caminos:
            return
        
        self.matriz = [fila[:] for fila in self.matriz_original]

        #Siguiente Camino
        self.camino_actual = (self.camino_actual + 1) % len(self.caminos)
        self.dibujar_matriz_especial(self.caminos[self.camino_actual], 'green')
        self.mostrar_mensaje(f"Mostrando camino {self.camino_actual + 1} de {len(self.caminos)}", 'info')

    #Encuentra los caminos mas corto, largo y optimo
    def encontrar_caminos_especiales(self):
        if not self.caminos:
            return
        self.caminos_especiales['corto'] = min(self.caminos, key=len)
        self.caminos_especiales['largo'] = max(self.caminos, key=len)
        self.caminos_especiales['optimo'] = self.encontrar_camino_optimo()

    def NodoInicio(self, fila, columna):
        if self.matriz[fila][columna] == 1:
        # En el caso de que hubiera una salida ya establecida, esta se eliminará
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[i])):
                    if self.matriz[i][j] == 2:
                        self.matriz[i][j] = 1
            # Se agrega la nueva salida en el laberinto
            self.matriz[fila][columna] = 2
            self.dibujar_matriz_especial([],None)
            self.mostrar_mensaje(f"Inicio establecido en ({fila}, {columna})", 'exito')

#-------------------------------------------------------------------
    """
    Selección inteligente del mejor camino:
    - Criterios combinados:
      1. Longitud (prioriza 25% más cortos)
      2. Eficiencia de movimiento (menos cambios de dirección)
    - Proceso:
      1. Ordena caminos por longitud
      2. Filtra los más cortos
      3. Evalúa cambios de dirección con calcular_cambios_direccion()
      4. Retorna el camino con menor número de giros
    """
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

        color = {
            'corto': 'green',
            'optimo': 'yellow',
            'largo': 'orange'
        }.get(tipo, 'green')
        self.dibujar_matriz_especial(self.caminos_especiales[tipo], color)
        self.mostrar_mensaje("Mostrando camino "+ tipo, 'info')

class JuegoLibre(JuegoBase):
    def __init__(self, root):
        super().__init__(root)
        self.setup_controles_libre()
        self.jugador_pos = None
        self.fin_pos = None
        self.juego_terminado = False
        self.bind_teclas()
        self.pasos = []
        self.resol = 0

    def setup_controles_libre(self):
            """Controles específicos del modo libre"""
            frame_controles = ttk.Frame(self.frame_controles)
            frame_controles.pack(side=tk.LEFT, padx=10)
        
            # Botón para seleccionar inicio
            
            ttk.Button(
                frame_controles,
                text="Seleccionar Inicio",
                command=self.modo_seleccion_inicio,
                style='TButton'
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                frame_controles,
                text="Resolucion",
                command=self.Resolucion,
                style='TButton'
            ).pack(side=tk.LEFT, padx=5)

            self.btn_siguiente = ttk.Button(
                frame_controles,
                text="Siguiente Camino",
                
                state=tk.DISABLED,
                style='TButton'
            )
            self.btn_siguiente.pack(side=tk.LEFT, padx=5)
            
            # Botón para reiniciar posición
            ttk.Button(
                frame_controles,
                text="Reiniciar Jugador",
                command=self.reiniciar_jugador,
                style='TButton'
            ).pack(side=tk.LEFT, padx=5)
            
            # Etiqueta de instrucciones
            self.label_instrucciones = ttk.Label(
                self.frame_controles,
                text="Usa las flechas del teclado para moverte",
                foreground='white',
                background='#3c3f41'
            )
            self.label_instrucciones.pack(side=tk.RIGHT, padx=10)

            if Guardado == False:
                self.botonGuardar = self.botonGuardar = ttk.Button(
                    self.frame_controles, 
                    text="Guardar Partida", 
                    command=self.guardar, 
                    state = tk.DISABLED,
                    style = 'TButton')
                self.botonGuardar.pack(side=tk.RIGHT, padx=5)

    def bind_teclas(self):
        self.juego.bind('<Up>', lambda e: self.mover_jugador(-1, 0))
        self.juego.bind('<Down>', lambda e: self.mover_jugador(1, 0))
        self.juego.bind('<Left>', lambda e: self.mover_jugador(0, -1))
        self.juego.bind('<Right>', lambda e: self.mover_jugador(0, 1))
        
    def generar_laberinto(self):
        global Guardado

        # 1) Si venimos de una partida guardada, solo limpiamos duplicados y tomamos start/end
        if Guardado:
            final = None
            for i, fila in enumerate(self.matriz):
                for j, val in enumerate(fila):
                    if val == 3: 
                        final  = [i, j]

            # borrar cualquier otro 2 o 3
            for i, fila in enumerate(self.matriz):
                for j, val in enumerate(fila):
                    if val == 2:
                        self.matriz[i][j] = 1
                    if val == 3 and [i,j] != final:
                        self.matriz[i][j] = 1


            self.jugador_pos = nodo_Aleatorio(self.matriz)
            self.inicioJ = self.jugador_pos
            self.matriz[self.jugador_pos[0]][self.jugador_pos[1]] = 2
            self.fin_pos  = final

        # 2) Si no hay partida guardada, generamos un laberinto nuevo y ponemos marcadores
        else:
            tamano = int(self.combo_dimensiones.get())
            self.matriz = crear_Matriz(tamano, modo_clasico=False)
            # posiciones aleatorias de inicio y fin
            self.jugador_pos = nodo_Aleatorio(self.matriz)
            self.inicioJ = self.jugador_pos
            self.fin_pos = nodo_Aleatorio(self.matriz)
            self.matriz[self.jugador_pos[0]][self.jugador_pos[1]] = 2
            self.matriz[self.fin_pos[0]][self.fin_pos[1]] = 3

        self.caminos, self.pasos = backtracking(self.matriz)

        if Guardado == False:
            self.botonGuardar.config(state=tk.NORMAL)

        # 3) Dibujamos la cuadrícula limpia
        for w in self.frame_laberinto.winfo_children():
            w.destroy()
        self.botones = []
        for i in range(len(self.matriz)):
            fila = []
            for j in range(len(self.matriz[0])):
                btn = tk.Button(
                    self.frame_laberinto, width=3, height=1,
                    relief="raised", font=('Arial', 10),
                    command=lambda x=i, y=j: self.NodoInicio(x, y)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                fila.append(btn)
            self.botones.append(fila)

        self.dibujar_matriz()
        self.mostrar_mensaje("Laberinto cargado" if Guardado else "Laberinto generado", 'exito')

    def modo_seleccion_inicio(self):
        """Selecciona punto inicial"""
        self.modo_seleccion = 'inicio'
        self.mostrar_mensaje("Haz clic en la celda de inicio", 'info')

    def NodoInicio(self, fila, columna):
        """Sobreescribe el método para selección manual"""
        if self.modo_seleccion == 'inicio':
            if self.matriz[fila][columna] == 1:
                self.establecer_inicio(fila, columna)
        elif self.modo_seleccion == 'fin':
            if self.matriz[fila][columna] == 1:
                self.establecer_fin(fila, columna)
        else:
            super().NodoInicio(fila, columna)

    def establecer_inicio(self, fila, columna):
        """Coloca al jugador en la posición inicial"""
        # Elimina posición anterior si existe
        if self.jugador_pos:
            i, j = self.jugador_pos
            self.matriz[i][j] = 1
            
        self.jugador_pos = [fila, columna]
        self.matriz[fila][columna] = 2  # 2 representa al jugador
        self.dibujar_matriz()
        self.mostrar_mensaje(f"Inicio establecido en ({fila}, {columna})", 'exito')

    def mover_jugador(self, dx, dy):
        """Mueve al jugador según las teclas presionadas"""
        if self.juego_terminado:
            return
        if not self.jugador_pos:
            self.mostrar_mensaje("Establece primero la posición inicial", 'error')
            return
            
        x, y = self.jugador_pos
        nuevo_x = x + dx
        nuevo_y =  y + dy
        
        # Verifica límites del laberinto
        if (0 <= nuevo_x < len(self.matriz)) and (0 <= nuevo_y < len(self.matriz[0])):
            # Verifica si es una celda transitable
            if self.matriz[nuevo_x][nuevo_y] in [1, 3]:  
                self.matriz[x][y] = 1  # Limpia la posición anterior
                self.jugador_pos = [nuevo_x, nuevo_y]
                
                # Verifica si llegó al final
                if self.fin_pos and nuevo_x == self.fin_pos[0] and nuevo_y == self.fin_pos[1]:
                    self.mostrar_mensaje("¡Felicidades! Llegaste al final", 'exito')
                    messagebox.showinfo("Enhorabuena", "¡Has llegado a la meta!!")
                    self.juego_terminado = True  # Aqui se marca que el juego termino
                    self.matriz[nuevo_x][nuevo_y] = 3


                else:
                    self.matriz[nuevo_x][nuevo_y] = 2  # Nueva posición
                self.matriz[self.inicioJ[0]][self.inicioJ[1]] = 5
                self.dibujar_matriz()
            else:
                self.mostrar_mensaje("Movimiento no permitido", 'error')
        else:
            self.mostrar_mensaje("No puedes salir del laberinto", 'error')

    def reiniciar_jugador(self):
        """Vuelve al jugador a la posición inicial"""
        if self.jugador_pos and self.matriz[self.jugador_pos[0]][self.jugador_pos[1]] == 2:
            self.matriz[self.jugador_pos[0]][self.jugador_pos[1]] = 1
            
        if self.fin_pos:
            self.matriz[self.fin_pos[0]][self.fin_pos[1]] = 3
            
        self.jugador_pos = self.inicioJ
        self.dibujar_matriz()
        self.mostrar_mensaje("Posición del jugador reiniciada", 'info')

    """
    Funcion que se encarga de inicializar la funcion de backtracking para la obtencion de pasos y camino del laberinto
    Además empieza la resolucion paso a paso
    En caso de no haber una matriz generada, se le mostrara un error 
    """
    def Resolucion(self):
        if self.matriz != None:
            self.resol = 0
            self.resolucionPaso()
            self.caminos, self.Pasos = backtracking(self.matriz)
        else:
            self.mostrar_mensaje("Debe de generar la matriz", 'Error')

    """
    De acuerdo con la lista pasos obtenida de la funcion backtracking
    Se recorre la lista de coordenadas, se busca la posicion en la matriz y se cambia el valor por un 4
    Se actualiza la interfaz del laberinto
    Se esperan 0.1s para hacer la siguiente llamada, esto con el fin de poder ver mejor el proceso
    """
    def resolucionPaso(self):
        if self.resol < len(self.pasos):
            i, j = self.pasos[self.resol]
            self.matriz[i][j] = 4         
            self.dibujar_matriz()
            self.resol += 1
            # programa la siguiente llamada dentro de 100 ms (0.1s)
            self.juego.after(100, self.resolucionPaso)
        else:
            self.mostrar_mensaje("Resolución completada", 'exito')

"""
    Validador de laberintos usando DFS:
    - Implementación:
      1. Matriz de visitados para evitar repeticiones
      2. Recorrido en profundidad desde (0,0)
      3. Prueba las 4 direcciones posibles
      4. Retorna True solo si alcanza la celda final
    - Eficiencia: O(n²) donde n es el tamaño de la matriz
"""
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

"""
Esta funcion rompe x cantidad de paredes 
- Logica de la funcion:
    1. Se cumple el ciclo dependiendo de la cantidad de veces establecida
    2. No se permiten mas de 100 intentos
    3. Se saca de manera aletoria un indice de la matriz
    4. Se valida que solo se pueda eliminar una pared que tenga 2 0 3 caminos alrededor
    5. Se eliminan las paredes que fueron debidamente validadas
- Parámetros Clave:
    1. tam: tamaño o largo de la matriz
    2. cantidad: Cuantas paredes se quieren romper 
    3. intentos: Cantidad de intentos que se realizan limite 100
    4. vecinosAbiertos: Posibles caminos alrededor de las paredes 
"""
def romperParedes(laberinto, cantidad):
    tam = len(laberinto)

    for _ in range(cantidad):
        intentos = 0
        while intentos < 100:
            fila = random.randint(1, tam - 2)
            columna = random.randint(1, tam - 2)

            # Esto hace posible que solo se puede eliminar una pared que este entre dos o tres caminos 
            if laberinto[fila][columna] == 0:
                vecinosAbiertos = 0
                if laberinto[fila-1][columna] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila+1][columna] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila][columna-1] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila][columna+1] == 1: 
                    vecinosAbiertos += 1
                
                if laberinto[fila-1][columna-1] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila-1][columna+1] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila+1][columna-1] == 1: 
                    vecinosAbiertos += 1
                if laberinto[fila+1][columna+1] == 1: 
                    vecinosAbiertos += 1

                if vecinosAbiertos == 2 or vecinosAbiertos ==3 :
                    laberinto[fila][columna] = 1
                    break

            intentos += 1

"""
Esta funcion genera un laberinto utilizando backtracking
- Logica de la funcion:
    1. Comienza desde la esquina superior izquierda 
    2. Crea caminos aleatorios al moverse dos celdas en direcciones posibles (arriba, abajo, izquierda, derecha), 
    3. Elimina las paredes intermedias entre celdas para crear nuevos caminos 
    4. Si no hay más caminos disponibles desde una posición, retrocede a la anterior (backtracking). 
    5. Se añade un borde de paredes alrededor del laberinto 
    6. Por ultimo, se marca una posición aleatoria como nodo final.
"""

def crear_Matriz(tamano, modo_clasico=True):
    if tamano % 2 == 0:
        tamano += 1

    # Crear una matriz llena de ceros (paredes)
    laberinto = [[0 for _ in range(tamano)] for _ in range(tamano)]

    # Comenzamos en la esquina superior izquierda
    inicio_fila = 0
    inicio_columna = 0
    laberinto[inicio_fila][inicio_columna] = 1 

    # Lista de posiciones
    pila = [(inicio_fila, inicio_columna)]

    direcciones = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    # Para verificar que las posiciones esten dentro del rango de la matriz
    def en_rango(fila, columna):
        return 0 <= fila < tamano and 0 <= columna < tamano

    # Aqui se generan los caminos de forma dinamica con backtracking
    while pila:
        fila_actual, columna_actual = pila[-1]

        vecinos = [] #Celdas a la que se puede mover desde la actual

        for d1, d2 in direcciones:
            nueva_fila = fila_actual + d1
            nueva_columna = columna_actual + d2

            if en_rango(nueva_fila, nueva_columna):
                if laberinto[nueva_fila][nueva_columna] == 0:
                    vecinos.append((nueva_fila, nueva_columna))

        if vecinos:
            siguiente_fila, siguiente_columna = random.choice(vecinos)

            # Quitar la pared entre la celda actual y la siguiente
            medio_fila = (fila_actual + siguiente_fila) // 2
            medio_columna = (columna_actual + siguiente_columna) // 2
            laberinto[medio_fila][medio_columna] = 1
            laberinto[siguiente_fila][siguiente_columna] = 1

            pila.append((siguiente_fila, siguiente_columna))
        else:
            pila.pop()

    laberinto[tamano - 1][tamano - 1] = 1
    laberinto[tamano - 2][tamano - 1] = 1
    laberinto[tamano - 1][tamano - 2] = 1

    # Primera fila de pared 
    ancho = len(laberinto[0])
    borde = [0] * (ancho + 2)

    laberinto_con_borde = [borde]  # primera fila de pared

    for fila in laberinto:
        laberinto_con_borde.append([0] + fila + [0])  # paredes a los lados

    laberinto_con_borde.append(borde)  # última fila de pared
   
    romperParedes(laberinto_con_borde, tamano//2)
    return laberinto_con_borde
    
"""
Esta funcion de backtracking busca todos los posibles caminos que hay para encontrar la salida.
Además la función guarda todos los pasos que se toman, probando distintos caminos hasta el primero que llegue a la función.
- Parámetros clave:
    * nodoAnterior: Evita movimientos redundantes
    * lista: Acumula el camino parcial actual
    * listaCaminos: Almacena soluciones completas
    * listaPasos: Almacena las coordenadas hasta encontrar el final
    * Final: valida que se encontro el final, esto para dejar de guardar coordenadas en listaPasos
"""
final = True
def backtracking(matriz):
    global final
    final = True
    listaCaminos = []
    visitados = []
    nodoInicio = []
    listaPasos = []
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor == 2:
                nodoInicio = [i, j]
    busqueda(matriz, None, nodoInicio, [], listaCaminos, visitados, listaPasos)
    return listaCaminos, listaPasos

"""
Función recursiva auxiliar para backtracking:
- Lógica de exploración:
    1. Marca celda actual como visitada
    2. Si llega al final (3), guarda el camino
    3. Explora en 4 direcciones (evitando retroceder)
    4. Implementa poda para evitar ciclos
    5. Todos los caminos son guardados y cada uno de los pasos que se hacen hasta llegar al final 
"""
def busqueda(matriz, nodoAnterior, nodoActual, lista, listaCaminos, visitados, listaPasos):
    global final
    if(nodoActual[0] >= 0 and nodoActual[1] >= 0 and nodoActual[0] < len(matriz) and nodoActual[1] < len(matriz)):
        for elem in visitados:
            if elem == nodoActual:
                return
        if final:
            listaPasos.append(nodoActual)
        
        if (matriz[nodoActual[0]][nodoActual[1]] == 3):
            listaCaminos += [lista + [nodoActual]]
            if final:
                final = False
        
        if (matriz[nodoActual[0]][nodoActual[1]] == 2 or matriz[nodoActual[0]][nodoActual[1]] == 1):
            visitados += [nodoActual]
            
            # Arriba
            tam = len(matriz)
            i = nodoActual[0]-1
            j = nodoActual[1]
            if (nodoAnterior != [i,j] and (0<=i<tam)and (0<=j<tam) and (matriz[i][j] ==1 or matriz[i][j] ==3)):
                busqueda(matriz, nodoActual, [i,j], lista + [nodoActual], listaCaminos, visitados, listaPasos,)
                if final:
                    listaPasos.append(nodoActual)
            # Derecha
            i = nodoActual[0]
            j = nodoActual[1]+1
            if (nodoAnterior != [i,j] and (0<=i<tam)and (0<=j<tam) and (matriz[i][j] ==1 or matriz[i][j] ==3)):
                busqueda(matriz, nodoActual, [i,j], lista + [nodoActual], listaCaminos, visitados, listaPasos)
                if final:
                    listaPasos.append(nodoActual)
            # Abajo
            i = nodoActual[0]+1
            j = nodoActual[1]
            if (nodoAnterior != [i,j] and (0<=i<tam)and (0<=j<tam) and (matriz[i][j] ==1 or matriz[i][j] ==3)):
                busqueda(matriz, nodoActual, [i,j], lista + [nodoActual], listaCaminos, visitados, listaPasos)
                if final:
                    listaPasos.append(nodoActual)
            # Izquierda
            i = nodoActual[0]
            j = nodoActual[1]-1
            if (nodoAnterior != [i,j] and (0<=i<tam)and (0<=j<tam) and (matriz[i][j] ==1 or matriz[i][j] ==3)):
                busqueda(matriz, nodoActual, [i,j], lista + [nodoActual], listaCaminos, visitados, listaPasos)
                if final:
                    listaPasos.append(nodoActual)

            visitados.pop()

"""
Funcion para elegir de manera aleatoria un punto en el mapa:
- Logica de la funcion:
    1. Recorre la matriz por medio de indices
    2. Se prueba que el elemento en la posicion sea igual a 1 (camino)
    3. Todos los indices de los caminos son agregados a la lista de posibles 
    4. Se utiliza de random para elegir uno de los puntos de la lista
- Parámetros Claves:
    * tam = tamaño o largo de la matriz
    * posibles = Guarda todos los puntos libres (caminos)
"""

def nodo_Aleatorio(matriz):
    tam = len(matriz)
    posibles = []
    for i in range(tam):
        for j in range(tam):
            if matriz[i][j] == 1:
                posibles.append([i, j])
    if posibles != None:
        return random.choice(posibles)

InterfazLaberinto()