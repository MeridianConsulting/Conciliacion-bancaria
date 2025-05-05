import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path
from PIL import Image, ImageTk

class BankSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica de la ventana - Aumentar resolución
        self.title("Meridian Consulting LTDA - Conciliación Bancaria")
        self.geometry("1200x800")  # Resolución aumentada
        self.minsize(1200, 800)    # Tamaño mínimo también ajustado
        
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
        
        # Mapeo de nombres de bancos a archivos de logo
        self.bank_logos = {
            'Itaú': 'itau.png',
            'BBVA': 'BBVA.png',
            'Bancolombia': 'Bancolombia.png',
            'Banco de Bogotá': 'BancoBogota.png',
            'Banco de Occidente': 'Occidente.png',
            'AV Villas': 'AvVillas.png',
            'Credicorp': 'Credicorp.png',
            'Corficolombiana': 'Corfi.jpeg',
            'Fiduciaria': 'Fidu.jpg'
        }
        
        # Lista de bancos disponibles
        self.available_banks = list(self.bank_logos.keys())
        
        # Variable para almacenar el banco seleccionado
        self.selected_bank = tk.StringVar()
        self.selected_bank.set("")  # Inicialmente ninguno seleccionado
        
        # Configurar el tema para la ventana
        self.configure(bg=self.colors['light_bg'])
        
        # Cargar fuentes modernas (fallback a fuentes del sistema si no están disponibles)
        self.fonts = {
            'title': ('Segoe UI', 22, 'bold'),    # Ligeramente reducido
            'subtitle': ('Segoe UI', 16, 'normal'),
            'body': ('Segoe UI', 12, 'normal'),   # Reducido
            'button': ('Segoe UI', 12, 'normal'), # Reducido
            'caption': ('Segoe UI', 10, 'normal'),
            'bank_name': ('Segoe UI', 14, 'bold') # Reducido
        }
        
        # Diccionario para almacenar las imágenes (evitar que se eliminen por el recolector de basura)
        self.images = {}
        
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
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        
        # Posicionar ventana
        self.geometry(f"1200x800+{x}+{y}")
    
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
        # Usar un contenedor vertical para organizar los elementos
        main_container = tk.Frame(self, bg=self.colors['light_bg'])
        main_container.pack(fill="both", expand=True)
        
        # =========== ENCABEZADO ===========
        header = tk.Frame(main_container, bg=self.colors['primary'])
        header.pack(fill="x", side="top")
        
        # Logos e iconos
        meridian_label = tk.Label(
            header,
            text="MERIDIAN CONSULTING",
            font=('Segoe UI', 18, 'bold'),  # Reducido
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        meridian_label.pack(side="left", padx=30, pady=12)  # Reducido
        
        # Título centrado
        title_label = tk.Label(
            header,
            text="Sistema de Conciliación Bancaria",
            font=('Segoe UI', 14),  # Reducido
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # =========== CONTENIDO PRINCIPAL ===========
        # Contenedor para organizar el contenido con altura máxima
        content_container = tk.Frame(main_container, bg=self.colors['light_bg'])
        content_container.pack(fill="both", expand=True, padx=20, pady=(15, 0))
        
        # Título de la sección con tipografía mejorada
        section_title = tk.Label(
            content_container,
            text="Seleccione su banco",
            font=self.fonts['title'],
            fg=self.colors['dark_text'],
            bg=self.colors['light_bg']
        )
        section_title.pack(pady=(0, 5))  # Reducido
        
        # Descripción simplificada
        description = tk.Label(
            content_container,
            text="Haga clic en la tarjeta del banco con el que desea realizar la conciliación",
            font=self.fonts['body'],
            fg=self.colors['secondary_text'],
            bg=self.colors['light_bg']
        )
        description.pack(pady=(0, 10))
        
        # =========== GRID DE BANCOS ===========
        # Frame contenedor para la cuadrícula de bancos
        banks_container = tk.Frame(content_container, bg=self.colors['light_bg'])
        banks_container.pack(fill="both", expand=True, padx=10, pady=5)  # Reducido
        
        # Configurar grid
        num_columns = 3
        for i in range(num_columns):
            banks_container.columnconfigure(i, weight=1)
        for i in range(3):  # 3 filas
            banks_container.rowconfigure(i, weight=1)
        
        # Cargar todas las imágenes primero
        self.load_bank_images()
        
        # Crear tarjetas para cada banco
        self.bank_buttons = {}
        
        for i, bank_name in enumerate(self.available_banks):
            row = i // num_columns
            col = i % num_columns
            
            # Crear marco exterior para tarjeta con padding
            card_outer = tk.Frame(
                banks_container,
                bg=self.colors['light_bg'],
                padx=5,  # Reducido
                pady=5   # Reducido
            )
            card_outer.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
            # Crear tarjeta con efecto de sombra y bordes redondeados
            card = tk.Frame(
                card_outer,
                bg=self.colors['white'],
                highlightbackground=self.colors['medium_gray'],
                highlightthickness=1,
                bd=0
            )
            card.pack(fill="both", expand=True)
            
            # Referencia al logo del banco
            logo_key = self.bank_logos[bank_name]
            
            # Crear contenedor cuadrado para el logo (tamaño fijo exactamente cuadrado)
            logo_size = 100  # REDUCIDO: Tamaño fijo en píxeles
            logo_container = tk.Frame(card, bg=self.colors['white'], width=logo_size, height=logo_size)
            logo_container.pack(pady=(10, 5))
            logo_container.pack_propagate(False)  # Mantener tamaño fijo
            
            # Si tenemos la imagen cargada, mostrarla
            if logo_key in self.images and self.images[logo_key]:
                # Imagen del logo
                logo_label = tk.Label(
                    logo_container,
                    image=self.images[logo_key],
                    bg=self.colors['white'],
                    bd=0
                )
                logo_label.place(relx=0.5, rely=0.5, anchor="center")  # Centrar logo
                
                # Nombre del banco debajo del contenedor de logo
                name_label = tk.Label(
                    card,
                    text=bank_name,
                    font=self.fonts['bank_name'],
                    fg=self.colors['dark_text'],
                    bg=self.colors['white']
                )
                name_label.pack(pady=(0, 10))
            else:
                # Fallback si no se puede cargar la imagen
                name_label = tk.Label(
                    logo_container,
                    text=bank_name,
                    font=self.fonts['bank_name'],
                    fg=self.colors['dark_text'],
                    bg=self.colors['white']
                )
                name_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Hacer que toda la tarjeta sea clickeable
            card.bind("<Button-1>", lambda e, b=bank_name: self.select_bank(b))
            logo_container.bind("<Button-1>", lambda e, b=bank_name: self.select_bank(b)) 
            logo_label.bind("<Button-1>", lambda e, b=bank_name: self.select_bank(b)) if 'logo_label' in locals() else None
            name_label.bind("<Button-1>", lambda e, b=bank_name: self.select_bank(b))
            
            # Cambiar cursor al pasar sobre elementos clickeables
            for widget in [card, logo_container, logo_label if 'logo_label' in locals() else None, name_label]:
                if widget:
                    widget.bind("<Enter>", lambda e, c=card: self.on_hover_enter(c))
                    widget.bind("<Leave>", lambda e, c=card: self.on_hover_leave(c))
                    widget.config(cursor="hand2")
            
            # Agregar a diccionario de botones
            self.bank_buttons[bank_name] = {
                'card': card,
                'outer': card_outer,
                'logo_container': logo_container
            }
        
        # =========== FOOTER CON BOTONES DE NAVEGACIÓN (FIJO) ===========
        # Footer siempre visible en la parte inferior
        footer_height = 120  # Altura ligeramente aumentada para el footer
        footer_frame = tk.Frame(main_container, bg=self.colors['light_bg'], height=footer_height)
        footer_frame.pack(side="bottom", fill="x", pady=(10, 10))
        footer_frame.pack_propagate(False)  # Impedir que el footer cambie su tamaño
        
        # Línea separadora destacada
        separator = tk.Frame(footer_frame, height=3, bg=self.colors['secondary'])
        separator.pack(fill="x", pady=(0, 15))
        
        # Contenedor para los botones de acción
        buttons_frame = tk.Frame(footer_frame, bg=self.colors['light_bg'], height=60)
        buttons_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        # Botón Salir (a la izquierda) con estilo mejorado
        self.exit_btn = tk.Button(
            buttons_frame,
            text="Salir",
            font=self.fonts['button'],
            fg=self.colors['white'],
            bg=self.colors['danger'],
            relief="raised",
            bd=2,
            padx=20,  # Reducido
            pady=10,  # Reducido
            cursor="hand2",
            command=self.on_closing
        )
        self.exit_btn.pack(side="left")
        
        # Añadir efectos hover al botón salir
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c82333"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg=self.colors['danger']))
        
        # Botón Continuar (a la derecha) con estilo mejorado
        self.continue_btn = tk.Button(
            buttons_frame,
            text="Continuar",
            font=self.fonts['button'],
            fg=self.colors['white'],
            bg=self.colors['success'] if self.selected_bank.get() else '#A0A0A0',  # Gris si deshabilitado
            relief="raised",
            bd=2,
            padx=20,  # Reducido
            pady=10,  # Reducido
            state='disabled',
            cursor="hand2" if self.selected_bank.get() else "arrow",
            command=self.on_continue
        )
        self.continue_btn.pack(side="right")
        
        # Añadir efectos hover al botón continuar (solo si está habilitado)
        def on_continue_enter(e):
            if self.continue_btn['state'] == 'normal':
                self.continue_btn.config(bg="#218838")
        
        def on_continue_leave(e):
            if self.continue_btn['state'] == 'normal':
                self.continue_btn.config(bg=self.colors['success'])
        
        self.continue_btn.bind("<Enter>", on_continue_enter)
        self.continue_btn.bind("<Leave>", on_continue_leave)
        
        # Copyright simplificado y centrado
        copyright_label = tk.Label(
            footer_frame,
            text="© 2024 Meridian Consulting LTDA.",
            font=self.fonts['caption'],
            fg=self.colors['secondary_text'],
            bg=self.colors['light_bg']
        )
        copyright_label.pack(side="bottom", pady=(0, 5))
    
    def load_bank_images(self):
        """Carga las imágenes de logos de bancos y las redimensiona apropiadamente"""
        # Directorio de assets
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets'))
        
        # Intentar cargar cada imagen
        for bank_name, logo_file in self.bank_logos.items():
            try:
                # Ruta completa al archivo
                image_path = os.path.join(assets_dir, logo_file)
                
                if os.path.exists(image_path):
                    try:
                        # Intentar cargar con PIL para redimensionar
                        from PIL import Image, ImageTk
                        
                        # Abrir y redimensionar la imagen
                        img = Image.open(image_path)
                        
                        # Tamaño fijo para logos
                        max_size = 80  # REDUCIDO: Tamaño para logos cuadrados
                        
                        # Calcular dimensiones manteniendo proporción
                        width, height = img.size
                        if width > height:
                            new_width = max_size
                            new_height = int(height * (max_size / width))
                        else:
                            new_height = max_size
                            new_width = int(width * (max_size / height))
                        
                        # Redimensionar
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Convertir a formato que tkinter pueda usar
                        photo = ImageTk.PhotoImage(img)
                        
                        # Guardar referencia
                        self.images[logo_file] = photo
                        
                    except ImportError:
                        # Fallback a tkinter nativo si PIL no está disponible
                        print("PIL no disponible, usando tkinter PhotoImage directamente")
                        photo = tk.PhotoImage(file=image_path)
                        self.images[logo_file] = photo
                else:
                    print(f"Archivo de logo no encontrado: {image_path}")
                    self.images[logo_file] = None
            except Exception as e:
                print(f"Error cargando logo {logo_file}: {e}")
                self.images[logo_file] = None
    
    def on_hover_enter(self, card):
        """Efecto al pasar el cursor sobre una tarjeta de banco"""
        try:
            # Encontrar a qué banco pertenece esta tarjeta
            bank_name = None
            for name, widgets in self.bank_buttons.items():
                if widgets['card'] == card:
                    bank_name = name
                    break
            
            if bank_name is None or bank_name == self.selected_bank.get():
                return  # No hacer nada si ya está seleccionado
            
            # Aplicar efecto de hover
            card.config(
                highlightbackground=self.colors['secondary'],
                highlightthickness=2
            )
        except Exception as e:
            print(f"Error en hover enter: {e}")
    
    def on_hover_leave(self, card):
        """Efecto al quitar el cursor de una tarjeta de banco"""
        try:
            # Encontrar a qué banco pertenece esta tarjeta
            bank_name = None
            for name, widgets in self.bank_buttons.items():
                if widgets['card'] == card:
                    bank_name = name
                    break
            
            if bank_name is None or bank_name == self.selected_bank.get():
                return  # No hacer nada si ya está seleccionado
            
            # Restaurar estado normal
            card.config(
                highlightbackground=self.colors['medium_gray'],
                highlightthickness=1
            )
        except Exception as e:
            print(f"Error en hover leave: {e}")
    
    def select_bank(self, bank_name):
        """Maneja la selección de un banco"""
        try:
            # Actualizar variable
            self.selected_bank.set(bank_name)
            
            # Resetear todos los botones
            for name, widgets in self.bank_buttons.items():
                card = widgets['card']
                
                if name == bank_name:
                    # Seleccionado: destacar con borde y efecto visual
                    card.config(
                        highlightbackground=self.colors['secondary'],
                        highlightthickness=3
                    )
                    # Añadir efecto de tarjeta seleccionada
                    card.config(relief="sunken")
                else:
                    # No seleccionado: restaurar estilo normal
                    card.config(
                        highlightbackground=self.colors['medium_gray'],
                        highlightthickness=1
                    )
                    # Restaurar relieve normal
                    card.config(relief="flat")
            
            # Habilitar botón continuar con estilo destacado
            self.continue_btn.config(
                state='normal',
                bg=self.colors['success'],
                cursor="hand2"
            )
            
            # Añadir un destello visual para indicar que se puede continuar
            # Guardar color original
            original_bg = self.continue_btn.cget("bg")
            # Hacer parpadear el botón brevemente
            def flash_button():
                # Cambiar a color de destello
                self.continue_btn.config(bg="#2fd151")  # Color más brillante
                # Programar retorno al color original
                self.after(200, lambda: self.continue_btn.config(bg=original_bg))
                # Programar segundo destello
                self.after(400, lambda: self.continue_btn.config(bg="#2fd151"))
                # Restaurar color final
                self.after(600, lambda: self.continue_btn.config(bg=original_bg))
            
            # Ejecutar destello
            self.after(100, flash_button)
            
            # Mostrar mensaje de confirmación
            print(f"Banco seleccionado: {bank_name}")
        except Exception as e:
            print(f"Error seleccionando banco: {e}")
    
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