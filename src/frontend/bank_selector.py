import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

class BankSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Meridian Consulting LTDA - Conciliación Bancaria")
        self.geometry("900x700")  # Ampliamos la ventana para mejor distribución
        self.minsize(900, 700)    # Tamaño mínimo también ajustado
        
        # Establecer el ícono si está disponible
        try:
            icon_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'logo.ico'))
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error cargando el ícono: {e}")
        
        # Paleta de colores (redefinida para mayor sofisticación)
        self.colors = {
            'primary': '#0A2F5C',       # Azul corporativo principal más oscuro
            'primary_light': '#1E4D84',  # Variante más clara del azul principal
            'secondary': '#0066B3',     # Azul corporativo secundario
            'accent': '#FFB81C',        # Color de acento dorado para destacados
            'light_bg': '#F8F9FA',      # Fondo muy claro (casi blanco)
            'light_gray': '#E9ECEF',    # Gris muy claro para fondos secundarios
            'medium_gray': '#CED4DA',   # Gris medio para bordes
            'dark_text': '#212529',     # Negro suave para texto principal
            'secondary_text': '#6C757D', # Gris para texto secundario
            'white': '#FFFFFF',         # Blanco puro
            'success': '#28a745',       # Verde para acciones positivas
            'danger': '#dc3545',        # Rojo para acciones de cancelación
            'danger_soft': '#F8D7DA',   # Rojo suavizado
            'card_shadow': '0 2px 8px rgba(0, 0, 0, 0.1)' # Sombra para tarjetas
        }
        
        # Colores para logos de bancos (con degradados suaves)
        self.bank_gradients = {
            'Itaú': ('linear-gradient(135deg, #EC7000, #FF8E29)', self.colors['white']),
            'BBVA': ('linear-gradient(135deg, #072146, #1A3C6E)', self.colors['white']),
            'Bancolombia': ('linear-gradient(135deg, #FFDD00, #EECC00)', self.colors['dark_text']),
            'Banco de Bogotá': ('linear-gradient(135deg, #144684, #1E5AA9)', self.colors['white']),
            'Banco de Occidente': ('linear-gradient(135deg, #E30613, #F02E3A)', self.colors['white']),
            'AV Villas': ('linear-gradient(135deg, #E31937, #F23D55)', self.colors['white']),
            'Credicorp': ('linear-gradient(135deg, #003865, #0A4D80)', self.colors['white']),
            'Corficolombiana': ('linear-gradient(135deg, #006341, #007A51)', self.colors['white']),
            'Fiduciaria': ('linear-gradient(135deg, #1D4289, #2857AC)', self.colors['white'])
        }
        
        # Lista de bancos disponibles
        self.available_banks = list(self.bank_gradients.keys())
        
        # Variable para almacenar el banco seleccionado
        self.selected_bank = tk.StringVar()
        self.selected_bank.set("")  # Inicialmente ninguno seleccionado
        
        # Configurar el tema para la ventana
        self.configure(bg=self.colors['light_bg'])
        
        # Cargar fuentes modernas (fallback a fuentes del sistema si no están disponibles)
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'subtitle': ('Segoe UI', 14, 'normal'),
            'body': ('Segoe UI', 12, 'normal'),
            'button': ('Segoe UI', 12, 'normal'),
            'caption': ('Segoe UI', 10, 'normal'),
            'bank_name': ('Segoe UI', 13, 'bold')
        }
        
        # Centrar la ventana
        self.center_window()
        
        # Crear contenido
        self.create_content()
        
        # Variable para rastrear si se ha seleccionado un banco
        self.bank_selected = False
        
        # Vincular evento de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variable para rastrear el último botón con hover
        self.hover_button = None
    
    def center_window(self):
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición
        x = (screen_width - 900) // 2
        y = (screen_height - 700) // 2
        
        # Posicionar ventana
        self.geometry(f"900x700+{x}+{y}")
    
    def create_rounded_frame(self, parent, bg_color='#FFFFFF', corner_radius=10, **kwargs):
        """Crea un frame con esquinas redondeadas usando un canvas"""
        
        # Frame base
        frame = tk.Frame(parent, bg=parent['bg'], **kwargs)
        
        # Canvas para dibujar el fondo redondeado
        canvas = tk.Canvas(
            frame,
            bg=parent['bg'],
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        
        # Actualizar canvas cuando cambie el tamaño
        def update_canvas(event):
            canvas.delete("all")
            w, h = event.width, event.height
            canvas.create_rectangle(
                corner_radius, 0, 
                w, h,
                fill=bg_color, outline="")
            canvas.create_rectangle(
                0, corner_radius, 
                w, h,
                fill=bg_color, outline="")
            canvas.create_arc(
                0, 0, 
                corner_radius*2, corner_radius*2,
                start=90, extent=90,
                fill=bg_color, outline="")
        
        canvas.bind("<Configure>", update_canvas)
        
        # Frame interior para contenido
        inner_frame = tk.Frame(frame, bg=bg_color)
        canvas.create_window(0, 0, anchor="nw", window=inner_frame, width=frame.winfo_reqwidth(), height=frame.winfo_reqheight())
        
        return frame, inner_frame
    
    def create_content(self):
        # =========== CONTAINER PRINCIPAL ===========
        main_container = tk.Frame(self, bg=self.colors['light_bg'])
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # =========== ENCABEZADO ===========
        header = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header.pack(fill="x", side="top", pady=(0, 30))
        
        # Logos e iconos
        meridian_label = tk.Label(
            header,
            text="MERIDIAN CONSULTING",
            font=('Segoe UI', 20, 'bold'),
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        meridian_label.pack(side="left", padx=30, pady=20)
        
        # Título centrado
        title_label = tk.Label(
            header,
            text="Sistema de Conciliación Bancaria",
            font=('Segoe UI', 16),
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # =========== CONTENIDO PRINCIPAL ===========
        content = tk.Frame(main_container, bg=self.colors['light_bg'])
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título de la sección con tipografía mejorada
        section_title = tk.Label(
            content,
            text="Seleccione su banco",
            font=self.fonts['title'],
            fg=self.colors['dark_text'],
            bg=self.colors['light_bg']
        )
        section_title.pack(anchor="center", pady=(0, 15))
        
        # Descripción simplificada
        description = tk.Label(
            content,
            text="Haga clic en la tarjeta del banco con el que desea realizar la conciliación",
            font=self.fonts['body'],
            fg=self.colors['secondary_text'],
            bg=self.colors['light_bg']
        )
        description.pack(anchor="center", pady=(0, 25))
        
        # =========== GRID DE BANCOS ===========
        # Frame contenedor para la cuadrícula de bancos
        banks_container = tk.Frame(content, bg=self.colors['light_bg'])
        banks_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid
        for i in range(3):
            banks_container.columnconfigure(i, weight=1)
        for i in range(3):
            banks_container.rowconfigure(i, weight=1)
        
        # Crear tarjetas para cada banco
        self.bank_buttons = {}
        
        for i, bank_name in enumerate(self.available_banks):
            row = i // 3
            col = i % 3
            
            # Crear marco exterior para tarjeta con padding
            card_outer = tk.Frame(
                banks_container,
                bg=self.colors['light_bg'],
                padx=10,
                pady=10
            )
            card_outer.grid(row=row, column=col, sticky="nsew")
            
            # Crear tarjeta con efecto de sombra y bordes redondeados
            card = tk.Frame(
                card_outer,
                bg=self.colors['white'],
                highlightbackground=self.colors['medium_gray'],
                highlightthickness=1,
                bd=0
            )
            card.pack(fill="both", expand=True)
            
            # Aplicar estilo de tarjeta
            bank_gradient, text_color = self.bank_gradients[bank_name]
            
            # Como no podemos usar CSS gradients, usamos colores sólidos
            bg_color = bank_gradient.split(', ')[1].replace(')', '')
            
            # Botón del banco con estilo mejorado
            btn = tk.Button(
                card,
                text=bank_name,
                font=self.fonts['bank_name'],
                fg=text_color,
                bg=bg_color,
                relief="flat",
                bd=0,
                padx=15,
                pady=20,
                cursor="hand2",  # Cursor de mano al pasar por encima
                command=lambda b=bank_name: self.select_bank(b)
            )
            btn.pack(fill="both", expand=True)
            
            # Agregar eventos para efectos hover
            btn.bind("<Enter>", lambda e, btn=btn, card=card: self.on_hover_enter(btn, card))
            btn.bind("<Leave>", lambda e, btn=btn, card=card: self.on_hover_leave(btn, card))
            
            # Agregar a diccionario de botones
            self.bank_buttons[bank_name] = {
                'button': btn,
                'card': card,
                'outer': card_outer
            }
        
        # =========== BOTONES DE ACCIÓN ===========
        # Frame para botones de navegación
        actions_frame = tk.Frame(main_container, bg=self.colors['light_bg'], height=70)
        actions_frame.pack(fill="x", side="bottom", pady=(25, 0))
        
        # Contenedor para alinear botones a la derecha
        buttons_container = tk.Frame(actions_frame, bg=self.colors['light_bg'])
        buttons_container.pack(side="right", padx=20)
        
        # Botón Salir
        self.exit_btn = tk.Button(
            buttons_container,
            text="Salir",
            font=self.fonts['button'],
            fg=self.colors['white'],
            bg=self.colors['danger'],
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.on_closing
        )
        self.exit_btn.pack(side="left", padx=(0, 15))
        
        # Dar efecto hover al botón salir
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c82333"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg=self.colors['danger']))
        
        # Botón Continuar
        self.continue_btn = tk.Button(
            buttons_container,
            text="Continuar",
            font=self.fonts['button'],
            fg=self.colors['white'],
            bg=self.colors['success'],
            relief="flat",
            padx=25,
            pady=10,
            state='disabled',
            cursor="hand2",
            command=self.on_continue
        )
        self.continue_btn.pack(side="left")
        
        # Dar efecto hover al botón continuar
        self.continue_btn.bind("<Enter>", lambda e: self.continue_btn.config(bg="#218838") if self.continue_btn['state'] == 'normal' else None)
        self.continue_btn.bind("<Leave>", lambda e: self.continue_btn.config(bg=self.colors['success']) if self.continue_btn['state'] == 'normal' else None)
        
        # =========== PIE DE PÁGINA SIMPLIFICADO ===========
        footer = tk.Frame(main_container, bg=self.colors['light_bg'], height=30)
        footer.pack(fill="x", side="bottom", pady=(15, 0))
        
        # Copyright simplificado y centrado
        copyright_label = tk.Label(
            footer,
            text="© 2024 Meridian Consulting LTDA.",
            font=self.fonts['caption'],
            fg=self.colors['secondary_text'],
            bg=self.colors['light_bg']
        )
        copyright_label.pack(pady=5)
    
    def on_hover_enter(self, button, card):
        """Efecto al pasar el cursor sobre un botón de banco"""
        # Guardar referencia al botón con hover actual
        self.hover_button = button
        
        # Aplicar efecto si no está seleccionado
        selected_btn = self.selected_bank.get()
        if button['text'] != selected_btn:
            # Efecto de elevación con borde
            card.config(
                highlightbackground=self.colors['secondary'],
                highlightthickness=2
            )
            # Pequeño efecto de escalado (simulado con padding)
            button.config(padx=13, pady=18)
    
    def on_hover_leave(self, button, card):
        """Efecto al quitar el cursor de un botón de banco"""
        # Quitar referencia al botón con hover
        self.hover_button = None
        
        # Restaurar estilo normal si no está seleccionado
        selected_btn = self.selected_bank.get()
        if button['text'] != selected_btn:
            card.config(
                highlightbackground=self.colors['medium_gray'],
                highlightthickness=1
            )
            button.config(padx=15, pady=20)
    
    def select_bank(self, bank_name):
        """Maneja la selección de un banco"""
        # Actualizar variable
        self.selected_bank.set(bank_name)
        
        # Resetear todos los botones
        for name, widgets in self.bank_buttons.items():
            button = widgets['button']
            card = widgets['card']
            
            if name == bank_name:
                # Seleccionado: destacar con borde y efecto visual
                card.config(
                    highlightbackground=self.colors['secondary'],
                    highlightthickness=3
                )
                # Efecto de presionado
                button.config(padx=13, pady=18)
            else:
                # No seleccionado: restaurar estilo normal
                card.config(
                    highlightbackground=self.colors['medium_gray'],
                    highlightthickness=1
                )
                button.config(padx=15, pady=20)
        
        # Habilitar botón continuar
        self.continue_btn.config(state='normal')
        
        # Mostrar banco seleccionado
        print(f"Banco seleccionado: {bank_name}")
    
    def on_continue(self):
        # Marcar que se ha seleccionado un banco
        self.bank_selected = True
        
        # Importante: terminar el mainloop pero mantener la ventana para que pueda ser accedida
        self.quit()
        
        # Imprimir mensaje de depuración 
        print("Selector de banco: Continuando con el banco " + self.selected_bank.get())
    
    def on_closing(self):
        # Terminar la aplicación
        self.quit()
        self.destroy() 